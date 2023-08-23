"""A CLI tool to manage contacts."""


import sys
from typing import Annotated, Any, Optional

import typer
from rich import box, print_json
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from contacts import contact, keyword
from contacts.address_book import AddressBook
from contacts.applescript_address_book import AppleScriptBasedAddressBook
from contacts.category import Category
from contacts.config import get_config
from contacts.field import ContactFieldMetadata, ContactFields, ContactInfoMetadata


class App(typer.Typer):
    """Typer application with a default command."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Make the first arg 'main', unless it is a known command."""
        if sys.argv[1] not in ["config"]:
            sys.argv = [sys.argv[0], "main", *sys.argv[1:]]
        return super().__call__(*args, **kwargs)


app = App(help=__doc__)


@app.command()
def config(show: bool = False, romanize: Optional[str] = None) -> None:
    """Manage configuration."""
    config = get_config()
    if romanize is not None:
        config.romanize = romanize
    config.dump()
    if show:
        print_json(config.json(), indent=4)


def with_icon(person: contact.Contact) -> str:
    """Contact with display icon."""
    return f"{person.category.icon} {person.name}"


def table(person: contact.Contact, width: Optional[int]) -> Table:
    """Create a table view for contact."""
    table = Table(highlight=True, box=box.ROUNDED, width=width)
    table.add_column(ratio=1, justify="right", style="magenta")
    table.add_column(person.category.icon)
    table.add_column(person.name, ratio=2)

    for field in ContactFields:
        value = field.value.get(person)
        if isinstance(field.value, ContactFieldMetadata):
            value = field.value.get(person)
            if not value:
                continue
            table.add_row(field.value.singular, field.value.category.icon, value)
        elif isinstance(field.value, ContactInfoMetadata):
            for index, info in enumerate(field.value.get(person)):
                if isinstance(info, contact.ContactInfo):
                    category = Category.from_label(info.label, field.value.category)
                    if category is None or category == Category.OTHER:
                        category = field.value.category
                    table.add_row(
                        field.value.plural if index == 0 else None,
                        category.icon,
                        str(info),
                    )

    for index, problem in enumerate(person.problems):
        table.add_row(
            "Problems" if index == 0 else None,
            problem.category.icon,
            problem.message,
        )

    return table


def get_address_book(brief: bool, batch: int) -> AddressBook:
    """Return an address book implementation given the configuration."""
    return AppleScriptBasedAddressBook(brief=brief, batch=batch)


@app.command()
def main(
    ctx: typer.Context,
    keywords: Annotated[Optional[list[str]], typer.Argument()] = None,
    *,
    detail: bool = False,
    json: bool = False,
    check: bool = False,
    fix: bool = False,
    batch: Optional[int] = None,
    width: Optional[int] = None,
    safe_box: bool = True,
) -> None:
    """Manage contacts matching given keyword."""
    if ctx.invoked_subcommand is not None:
        return

    console = Console(width=width, safe_box=safe_box)
    with Progress(transient=True, console=console) as progress:
        task = progress.add_task("Counting contacts")
        keywords = keyword.prepare_keywords(keywords or [])

        address_book = get_address_book(
            brief=not (detail or json or check or fix),
            batch=batch or (1 if keywords else 10),
        )
        count = address_book.count(keywords)
        progress.update(task, total=count, description="Fetching contacts")

        people = contact.Contacts()
        for person in address_book.find(keywords):
            if fix:
                for problem in person.problems:
                    progress.update(task, description=f"Fixing {with_icon(person)}")
                    problem.try_fix(address_book)
                person = address_book.get(person.contact_id)

            if detail:
                console.print(table(person, width))
            elif not json:
                console.print(f"{with_icon(person)}")

            people.contacts.append(person)
            progress.update(task, advance=1, description="Fetching contacts")

        if json:
            console.print_json(people.dumps(), indent=4)


if __name__ == "__main__":
    app()

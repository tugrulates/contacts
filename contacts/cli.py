"""A CLI tool to manage contacts."""


import dataclasses
from typing import Annotated, Optional

import typer
from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from contacts import contact, keyword
from contacts.address_book import AddressBook
from contacts.applescript_address_book import AppleScriptBasedAddressBook
from contacts.category import Category

app = typer.Typer(help=__doc__)


def with_icon(person: contact.Contact) -> str:
    """Contact with display icon."""
    return f"{person.category.icon} {person.name}"


def table(person: contact.Contact, width: Optional[int]) -> Table:
    """Create a table view for contact."""
    table = Table(highlight=True, box=box.ROUNDED, width=width)
    table.add_column(ratio=1, justify="right", style="magenta")
    table.add_column(person.category.icon)
    table.add_column(person.name, ratio=2)

    for field in dataclasses.fields(person):
        metadata = contact.Contact.metadata(field.name)
        value = getattr(person, field.name)
        if not (metadata and value):
            continue
        if isinstance(value, list):
            for index, info in enumerate(value):
                if isinstance(info, contact.ContactInfo):
                    info_category = Category.from_label(info.label)
                    table.add_row(
                        metadata.plural() if index == 0 else None,
                        (info_category or metadata.category).icon,
                        str(info),
                    )
        else:
            table.add_row(metadata.singular, metadata.category.icon, value)

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
def find(
    keywords: Annotated[Optional[list[str]], typer.Argument()] = None,
    *,
    extend: bool = True,
    detail: bool = False,
    json: bool = False,
    check: bool = False,
    fix: bool = False,
    applescript: bool = True,
    batch: Optional[int] = None,
    width: Optional[int] = None,
    safe_box: bool = True,
) -> None:
    """List contacts matching given keyword."""
    console = Console(width=width, safe_box=safe_box)
    with Progress(transient=True) as progress:
        task = progress.add_task("Counting contacts")
        keywords = keywords or []
        if applescript:
            keywords = keyword.prepare_keywords(keywords, extend=extend)

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
            print(people.dumps())


if __name__ == "__main__":
    app()

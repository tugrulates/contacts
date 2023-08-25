"""A CLI tool to manage contacts."""

import sys
from typing import Annotated, Any, Optional

import typer
from rich import box, print_json
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from contacts import address_book, config, contact, keyword
from contacts.address import AddressFormat, SemanticAddressField
from contacts.category import Category
from contacts.field import ContactFieldMetadata, ContactFields, ContactInfoMetadata


class App(typer.Typer):
    """Typer application with a default command."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Make the first arg 'main', unless it is a known command."""
        if len(sys.argv) > 1 and sys.argv[1] not in [
            "config",
            "--install-completion",
            "--show-completion",
        ]:
            sys.argv = [sys.argv[0], "main", *sys.argv[1:]]
        return super().__call__(*args, **kwargs)


app = App(help=__doc__)


@app.command(name="config")
def configure(
    show: bool = False,
    romanize: Optional[str] = None,
    address_format_country_code: Optional[str] = None,
    address_format_street: Optional[SemanticAddressField] = None,
    address_format_city: Optional[SemanticAddressField] = None,
    address_format_state: Optional[SemanticAddressField] = None,
    address_format_zip_code: Optional[SemanticAddressField] = None,
    mapquest_api_key: Optional[str] = None,
) -> None:
    """Manage configuration."""
    cfg = config.get_config()
    if romanize is not None:
        cfg.romanize = romanize
    if mapquest_api_key is not None:
        cfg.mapquest_api_key = mapquest_api_key
    if address_format_country_code is not None:
        cfg.address_formats[address_format_country_code] = AddressFormat(
            street=address_format_street,
            city=address_format_city,
            state=address_format_state,
            zip_code=address_format_zip_code,
        )
    cfg.dump()
    if show:
        print_json(cfg.model_dump_json(), indent=4)


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

        addr_book = address_book.get_address_book(
            brief=not (detail or json or check or fix),
            batch=batch or (1 if keywords else 10),
        )
        count = addr_book.count(keywords)
        progress.update(task, total=count, description="Fetching contacts")

        people = contact.Contacts()
        for person in addr_book.find(keywords):
            if fix:
                for problem in person.problems:
                    progress.update(task, description=f"Fixing {with_icon(person)}")
                    problem.try_fix(addr_book)
                person = addr_book.get(person.id)

            if detail:
                console.print(table(person, width))
            elif not json:
                console.print(f"{with_icon(person)}")

            people.contacts.append(person)
            progress.update(task, advance=1, description="Fetching contacts")

        if json:
            console.print_json(people.model_dump_json(exclude_defaults=True), indent=4)


if __name__ == "__main__":
    app()

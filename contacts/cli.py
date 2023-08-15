"""A CLI tool to manage contacts."""


import dataclasses
from typing import Annotated, Optional

import typer
from rich import box, print
from rich.progress import Progress
from rich.table import Table

from contacts import address_book, contact, keyword
from contacts.category import Category

app = typer.Typer(help=__doc__)


def with_icon(person: contact.Contact) -> str:
    """Contact with display icon."""
    return f"{person.category.icon} {person.name}"


def table(person: contact.Contact, width: Optional[int], safe_box: bool) -> Table:
    """Create a table view for contact."""
    table = Table(highlight=True, box=box.ROUNDED, width=width, safe_box=safe_box)
    table.add_column(ratio=1, justify="right", style="magenta")
    table.add_column(person.category.icon)
    table.add_column(person.name, ratio=2)

    for field in dataclasses.fields(contact.Contact):
        field_key = field.name.capitalize().replace("_", " ")
        field_value = getattr(person, field.name)
        field_category = Category.from_field(field)
        if not (field_value and field_category):
            continue
        if isinstance(field_value, list):
            for index, info in enumerate(field_value):
                if isinstance(info, contact.ContactInfo):
                    info_category = Category.from_label(info.label)
                    table.add_row(
                        field_key if index == 0 else None,
                        (info_category or field_category).icon,
                        str(info),
                    )
        else:
            table.add_row(field_key, field_category.icon, field_value)

    for index, problem in enumerate(person.problems):
        table.add_row(
            "Problems" if index == 0 else None,
            problem.category.icon,
            problem.message,
        )

    return table


@app.command()
def find(
    keywords: Annotated[Optional[list[str]], typer.Argument()] = None,
    *,
    extend: bool = True,
    detail: bool = False,
    check: bool = False,
    fix: bool = False,
    batch: Optional[int] = None,
    width: Optional[int] = None,
    safe_box: bool = True,
) -> None:
    """List contacts matching given keyword."""
    with Progress(transient=True) as progress:
        task = progress.add_task("Counting contacts")
        keywords = keyword.prepare_keywords(keywords or [], extend=extend)
        count = address_book.count(keywords)
        brief = not (detail or check or fix)
        batch = batch or (1 if keywords else 10)
        progress.update(task, total=count, description="Fetching contacts")

        for person in address_book.by_keyword(keywords, brief=brief, batch=batch):
            if fix:
                for problem in person.problems:
                    progress.update(task, description=f"Fixing {with_icon(person)}")
                    problem.try_fix()
                person = address_book.reload(person)
            print(table(person, width, safe_box) if detail else f"{with_icon(person)}")
            del person.first_name
            progress.update(task, advance=1, description="Fetching contacts")


if __name__ == "__main__":
    app()

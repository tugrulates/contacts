"""A CLI tool to manage contacts."""


from typing import Annotated, Optional

import typer
from rich import box, print
from rich.progress import Progress
from rich.table import Table

from contacts import address_book, contact, keyword

DETAILS = [
    "prefix",
    "first_name",
    "phonetic_first_name",
    "middle_name",
    "phonetic_middle_name",
    "last_name",
    "phonetic_last_name",
    "maiden_name",
    "suffix",
    "nickname",
    "job_title",
    "department",
    "organization",
    "phones",
    "emails",
    "home_page",
    "urls",
    "addresses",
    "birth_date",
    "custom_dates",
    "related_names",
    "social_profiles",
    "instant_messages",
    "note",
    "problems",
]

app = typer.Typer(help=__doc__)


def table(person: contact.Contact, width: Optional[int], safe_box: bool) -> Table:
    """Create a table view for contact."""
    table = Table(highlight=True, box=box.ROUNDED, width=width, safe_box=safe_box)
    table.add_column(ratio=1, justify="right", style="magenta")
    table.add_column(str(person), ratio=2)

    details = {prop: person.__getattribute__(prop) for prop in DETAILS}
    for key, value in details.items():
        if not value:
            continue
        if isinstance(value, list):
            value = "\n".join(map(str, value))
        else:
            value = str(value)
        table.add_row(key.replace("_", " ").capitalize(), value)

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
                    progress.update(task, description=f"Fixing {person}")
                    problem.try_fix()
                person = address_book.reload(person)
            print(table(person, width, safe_box) if detail else person)
            progress.advance(task)


if __name__ == "__main__":
    app()

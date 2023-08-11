"""A CLI tool to manage contacts."""


from typing import Annotated, Optional

import typer
from rich import box, print
from rich.progress import Progress
from rich.table import Table

from contacts import contact, keyword

ALL_CONTACTS: list[str] = []

# App object enclosing the commands.
app = typer.Typer(help=__doc__)


@app.command()
def find(
    keywords: Annotated[Optional[list[str]], typer.Argument()] = None,
    *,
    batch: int = 1,
    extend: bool = True,
    detail: bool = False,
    safe_box: bool = True,
) -> None:
    """List contacts matching given keyword."""
    with Progress(transient=True) as progress:
        task = progress.add_task("Counting contacts")
        keywords = keyword.prepare_keywords(keywords or [], extend=extend)
        count = contact.count(keywords)
        progress.update(task, total=count, description="Fetching contacts")

        for person in contact.by_keyword(keywords, batch=batch):
            if not detail:
                print(person)
            else:
                table = Table(highlight=True, box=box.ROUNDED, safe_box=safe_box)
                table.add_column(min_width=20, justify="right", style="magenta")
                table.add_column(str(person))
                for key, value in person.details().items():
                    if isinstance(value, list):
                        value = "\n".join(map(str, value))
                    else:
                        value = str(value)
                    table.add_row(key.replace("_", " ").capitalize(), value)
                print(table)

            progress.advance(task)


if __name__ == "__main__":
    app()

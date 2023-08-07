"""A CLI tool to manage contacts."""


from typing import Annotated, Optional

import typer

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
) -> None:
    """List contacts matching given keyword."""
    keywords = keyword.prepare(keywords or [], extend=extend)
    for person in contact.by_keyword(keywords, batch=batch):
        print(
            "{} {}".format(
                ["  ", ["👤", "🏢"][person.is_company]][person.has_image],
                person.name,
            )
        )


if __name__ == "__main__":
    app()

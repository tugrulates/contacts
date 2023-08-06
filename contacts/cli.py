"""A CLI tool to manage contacts."""


from typing import Annotated, Optional

import typer

from contacts import contact

ALL_CONTACTS: list[str] = []

# App object enclosing the commands.
app = typer.Typer(help=__doc__)


@app.command()
def find(keywords: Annotated[Optional[list[str]], typer.Argument()] = None) -> None:
    """List contacts matching given keyword."""
    for person in contact.by_keyword(keywords or []):
        print(
            "{} {}".format(
                ["  ", ["👤", "🏢"][person.is_company]][person.has_image],
                person.name,
            )
        )


if __name__ == "__main__":
    app()

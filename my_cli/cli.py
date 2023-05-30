"""Help message for my CLI app. Change this."""


import random
from pathlib import Path
from typing import Optional

import typer

APP_NAME = "my-cli"  # change this


# App object enclosing the commands.
app = typer.Typer(help=__doc__)


@app.command()
def quote(favorite: Optional[str] = None) -> None:
    """Print a random quote from Zoolander."""
    # Static files will be in site-packages next to this file.
    quotes_path = Path(__file__).parent / "static" / "my_quotes.txt"
    quotes = quotes_path.read_text(encoding="utf-8").strip().split("\n")

    # Filter quotes using the favorite filter.
    if favorite:
        quotes = [x for x in quotes if favorite.lower() in x.lower()]

    # Random number generators in the standard library are not suitable for security.
    # Drop the 'nosec' below and run 'hatch run lint:lint' to see lint checks in action.
    print(random.choice(quotes or ["You've done nothing! NOTHIIIING!"]))  # nosec


if __name__ == "__main__":
    app()

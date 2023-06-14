"""A CLI tool to manage contacts."""


import typer

from contacts import contact

# App object enclosing the commands.
app = typer.Typer(help=__doc__)


@app.command()
def find(keywords: list[str]) -> None:
    """List contacts matching given keyword."""
    for person in contact.find(keywords):
        print(
            "{} {}".format(
                ["  ", ["👤", "🏢"][person.is_company]][person.has_image],
                person.name,
            )
        )


if __name__ == "__main__":
    app()

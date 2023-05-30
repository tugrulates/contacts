"""Unittests for the CLI."""


from typer.testing import CliRunner

from my_cli import cli

runner = CliRunner()


def test_help() -> None:
    """Test help."""
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout


def test_quote() -> None:
    """Test Zoolander quote."""
    result = runner.invoke(cli.app)
    assert result.exit_code == 0
    assert len(result.stdout.strip().split("\n")) == 1


def test_favorite_quote() -> None:
    """Test Zoolander quote."""
    result = runner.invoke(cli.app, ["--favorite=break-dance"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "They're break-dance fighting."


def test_favorite_quote_missing() -> None:
    """Test Zoolander quote."""
    result = runner.invoke(cli.app, ["--favorite=derek"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "You've done nothing! NOTHIIIING!"

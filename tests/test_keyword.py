"""Unittests for keyword."""

from typer.testing import CliRunner

from contacts import keyword

runner = CliRunner(mix_stderr=True)


def test_prepare() -> None:
    """Test non-extended prepare."""
    assert keyword.prepare(["amelia", "bob"]) == ["Amelia", "Bob"]
    assert keyword.prepare(["bob", "amelia"]) == ["Amelia", "Bob"]
    assert keyword.prepare(["carnival balloon"]) == ["Carnival Balloon"]


def test_prepare_extend() -> None:
    """Test non-extended prepare."""
    assert keyword.prepare(["BOB"]) == ["Bob"]
    assert keyword.prepare(["BoB"]) == ["Bob"]
    assert keyword.prepare(["bob"], extend=True) == ["Bob", "Böb"]
    assert keyword.prepare(["balloon"], extend=True) == [
        "Balloon",
        "Balloön",
        "Ballöon",
        "Ballöön",
    ]

"""Unittests for keyword."""

from typer.testing import CliRunner

from contacts import keyword

runner = CliRunner(mix_stderr=True)


def test_prepare() -> None:
    """Test non-extended prepare."""
    assert keyword.prepare_keywords(["amelia", "bob"]) == ["Amelia", "Bob"]
    assert keyword.prepare_keywords(["bob", "amelia"]) == ["Amelia", "Bob"]
    assert keyword.prepare_keywords(["carnival balloon"]) == ["Carnival Balloon"]


def test_prepare_extend() -> None:
    """Test non-extended prepare."""
    assert keyword.prepare_keywords(["BOB"]) == ["Bob"]
    assert keyword.prepare_keywords(["BoB"]) == ["Bob"]
    assert keyword.prepare_keywords(["bob"], extend=True) == ["Bob", "Böb"]
    assert keyword.prepare_keywords(["balloon"], extend=True) == [
        "Balloon",
        "Balloön",
        "Ballöon",
        "Ballöön",
    ]

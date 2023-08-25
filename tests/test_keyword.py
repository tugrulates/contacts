"""Unit tests for keyword."""

from typer.testing import CliRunner

from contacts import config, keyword

runner = CliRunner(mix_stderr=True)


def test_prepare() -> None:
    """Test non-extended prepare."""
    assert keyword.prepare_keywords(["amelia", "bob"]) == ["Amelia", "Bob"]
    assert keyword.prepare_keywords(["bob", "amelia"]) == ["Amelia", "Bob"]
    assert keyword.prepare_keywords(["carnival balloon"]) == ["Carnival Balloon"]


def test_prepare_romanize(mock_config: config.Config) -> None:
    """Test non-extended prepare."""
    mock_config.romanize = "öøÑ"
    keyword.romanization.cache_clear()
    assert keyword.romanization() == {"n": ["ñ"], "o": ["ö", "ø"]}
    assert set(keyword.prepare_keywords(["BOB"])) == {"Bob", "Böb", "Bøb"}
    assert set(keyword.prepare_keywords(["BoB"])) == {"Bob", "Böb", "Bøb"}
    assert set(keyword.prepare_keywords(["bob"])) == {"Bob", "Böb", "Bøb"}
    assert set(keyword.prepare_keywords(["balloon"])) == {
        "Balloon",
        "Ballooñ",
        "Balloön",
        "Balloöñ",
        "Balloøn",
        "Balloøñ",
        "Ballöon",
        "Ballöoñ",
        "Ballöön",
        "Ballööñ",
        "Ballöøn",
        "Ballöøñ",
        "Balløon",
        "Balløoñ",
        "Balløön",
        "Balløöñ",
        "Balløøn",
        "Balløøñ",
    }

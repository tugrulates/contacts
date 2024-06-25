"""Unittests for query."""

import importlib

import pytest
from typer.testing import CliRunner

from contacts import config, query

runner = CliRunner(mix_stderr=True)


@pytest.fixture(autouse=True)
def cfg(monkeypatch: pytest.MonkeyPatch) -> config.Config:
    """Initialize the test configuration."""
    cfg = config.Config()
    monkeypatch.setattr(config, "get_config", lambda: cfg)
    importlib.reload(query)
    return cfg


def test_prepare() -> None:
    """Test non-extended prepare."""
    assert query.prepare_keywords(["amelia", "bob"]) == ["Amelia", "Bob"]
    assert query.prepare_keywords(["bob", "amelia"]) == ["Amelia", "Bob"]
    assert query.prepare_keywords(["carnival balloon"]) == ["Carnival Balloon"]


def test_prepare_romanize(cfg: config.Config) -> None:
    """Test non-extended prepare."""
    cfg.romanize = "öøÑ"
    assert query.romanization() == {"n": ["ñ"], "o": ["ö", "ø"]}
    assert set(query.prepare_keywords(["BOB"])) == {"Bob", "Böb", "Bøb"}
    assert set(query.prepare_keywords(["BoB"])) == {"Bob", "Böb", "Bøb"}
    assert set(query.prepare_keywords(["bob"])) == {"Bob", "Böb", "Bøb"}
    assert set(query.prepare_keywords(["balloon"])) == {
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

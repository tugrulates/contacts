"""Unittests for cli."""

import importlib
import json
from pathlib import Path

import email_validator
import pytest
from typer.testing import CliRunner

from contacts import cli, config
from contacts.checks import url_check
from contacts.contact import Contact
from tests.contact_diff import ContactDiff
from tests.mock_address_book import MockAddressBook

runner = CliRunner()


@pytest.fixture(scope="session", autouse=True)
def environment() -> None:
    """Initialize the test environment."""
    # disable DNS checks for e-mail address and URL checks
    email_validator.TEST_ENVIRONMENT = True
    url_check.TEST_ENVIRONMENT = True


@pytest.fixture(autouse=True)
def cfg(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> config.Config:
    """Initialize the test configuration."""
    monkeypatch.setattr(config, "CONFIG_PATH", tmp_path / "config.json")
    cfg = config.Config()
    cfg.dump()
    importlib.reload(cli)
    return cfg


@pytest.fixture(autouse=True)
def data_path(request: pytest.FixtureRequest) -> Path:
    """Fixture for the test data directory."""
    return request.path.parent / "data"


@pytest.fixture(autouse=True)
def mock_address_book(
    data_path: Path, monkeypatch: pytest.MonkeyPatch
) -> MockAddressBook:
    """Fixture for mock address book."""
    mock = MockAddressBook(data_path)
    monkeypatch.setattr(cli, "get_address_book", lambda *args, **kwargs: mock)
    return mock


def test_bare() -> None:
    """Test invocation with no arguments."""
    result = runner.invoke(cli.app, ["main"])
    assert result.exit_code == 0
    assert not result.stdout.strip()


def test_help() -> None:
    """Test help."""
    result = runner.invoke(cli.app, "main --help")
    assert result.exit_code == 0
    assert "Usage:" in result.stdout


def test_config() -> None:
    """Test setting config."""
    result = runner.invoke(cli.app, "config --romanize öøÑ")
    assert result.exit_code == 0
    assert not result.stdout.strip()
    assert config.get_config() == config.Config(romanize="öøÑ")


def test_config_show() -> None:
    """Test showing config."""
    result = runner.invoke(cli.app, "config --show --romanize öøÑ")
    assert result.exit_code == 0
    assert result.stdout.strip().split("\n") == [
        "{",
        '    "romanize": "öøÑ"',
        "}",
    ]


def test_applescript_error(mock_address_book: MockAddressBook) -> None:
    """Test applescript error."""
    mock_address_book.error()
    result = runner.invoke(cli.app, "main amelie")
    assert result.exit_code == 1


def test_all_contacts(mock_address_book: MockAddressBook) -> None:
    """Test find with no keywords returning all contacts."""
    mock_address_book.provide("amelie", "bob", "carnival")
    result = runner.invoke(cli.app, "main waldo")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_single_contact(mock_address_book: MockAddressBook) -> None:
    """Test find with single contact."""
    mock_address_book.provide("amelie")
    result = runner.invoke(cli.app, "main amelie")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
    ]


def test_multiple_contact(mock_address_book: MockAddressBook) -> None:
    """Test find with multiple contacts."""
    mock_address_book.provide("bob", "carnival")
    result = runner.invoke(cli.app, "main balloon")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_multiple_keywords(mock_address_book: MockAddressBook) -> None:
    """Test find with single contact."""
    mock_address_book.provide("amelie", "bob")
    result = runner.invoke(cli.app, "main amelie bob")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
    ]


def test_warnings(mock_address_book: MockAddressBook) -> None:
    """Test reporting warnings."""
    mock_address_book.provide("warnen")
    result = runner.invoke(cli.app, "main --check")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "⚠️  dr. warnen bitte sanft jr.",
    ]


def test_fix_warnings(data_path: Path, mock_address_book: MockAddressBook) -> None:
    """Test fixing warnings."""
    mock_address_book.provide("warnen")
    result = runner.invoke(cli.app, "main --fix")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "⚠️  dr. warnen bitte sanft jr.",
    ]
    before = Contact.load(data_path / "warnen.json")
    after = Contact.load(data_path / "warnen.fixed.json")
    diff = ContactDiff(before, after)
    assert sorted(mock_address_book.updates) == sorted(diff.updates)
    assert sorted(mock_address_book.adds) == sorted(diff.adds)
    assert sorted(mock_address_book.deletes) == sorted(diff.deletes)


def test_errors(mock_address_book: MockAddressBook) -> None:
    """Test reporting errors."""
    mock_address_book.provide("errona")
    result = runner.invoke(cli.app, "main --check")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "⛔ Errona Tragedia",
    ]


def test_detail_single(data_path: Path, mock_address_book: MockAddressBook) -> None:
    """Test detail with single contact."""
    mock_address_book.provide("amelie")
    result = runner.invoke(cli.app, "main --detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = (data_path / "amelie.detail").read_text(encoding="utf-8").strip()
    assert result.stdout.strip() == expected_output


def test_detail_multiple(data_path: Path, mock_address_book: MockAddressBook) -> None:
    """Test detail with multiple contacts."""
    mock_address_book.provide("amelie", "bob", "carnival")
    result = runner.invoke(cli.app, "main --detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = "\n".join(
        (data_path / x).with_suffix(".detail").read_text(encoding="utf-8").strip()
        for x in ["amelie", "bob", "carnival"]
    )
    assert result.stdout.strip() == expected_output


def test_detail_warnings(data_path: Path, mock_address_book: MockAddressBook) -> None:
    """Test warnings on detail."""
    mock_address_book.provide("warnen")
    result = runner.invoke(cli.app, "main warnen --detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = (data_path / "warnen.detail").read_text(encoding="utf-8").strip()
    assert result.stdout.strip() == expected_output


def test_detail_errors(data_path: Path, mock_address_book: MockAddressBook) -> None:
    """Test errors on detail."""
    mock_address_book.provide("errona")
    result = runner.invoke(cli.app, "main errona --detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = (data_path / "errona.detail").read_text(encoding="utf-8").strip()
    assert result.stdout.strip() == expected_output


def test_json(data_path: Path, mock_address_book: MockAddressBook) -> None:
    """Test detail with multiple contacts."""
    mock_address_book.provide("amelie", "bob", "carnival")
    result = runner.invoke(cli.app, "main --json --width=1000")
    assert result.exit_code == 0
    contacts = [
        json.loads(Path(data_path / x).read_text(encoding="utf-8"))
        for x in ["amelie.json", "bob.json", "carnival.json"]
    ]
    expected = json.dumps({"contacts": contacts}, indent=4, ensure_ascii=False)
    assert result.stdout.strip() == expected

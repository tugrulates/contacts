"""Unittests for cli."""


from pathlib import Path

import pytest
from typer.testing import CliRunner

from contacts import address_book, cli
from contacts.contact import Contact
from tests.contact_diff import ContactDiff
from tests.mocks import MockApplescript

runner = CliRunner(mix_stderr=True)


@pytest.fixture(autouse=True)
def data_path(request: pytest.FixtureRequest) -> Path:
    """Test data directory."""
    return request.path.parent / "data"


@pytest.fixture(autouse=True)
def mock_applescript(
    data_path: Path, monkeypatch: pytest.MonkeyPatch
) -> MockApplescript:
    """Fixture for prefs."""
    mock = MockApplescript(data_path)
    monkeypatch.setattr(address_book, "_run_and_read_output", mock._run_and_read_output)
    monkeypatch.setattr(address_book, "_run_and_read_log", mock._run_and_read_log)
    return mock


def test_bare() -> None:
    """Test invocation with no arguments."""
    result = runner.invoke(cli.app)
    assert result.exit_code == 0
    assert not result.stdout.strip()


def test_help() -> None:
    """Test help."""
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout


def test_applescript_error(mock_applescript: MockApplescript) -> None:
    """Test applescript error."""
    mock_applescript.error()
    result = runner.invoke(cli.app, "amelia")
    assert result.exit_code == 1


def test_all_contacts(mock_applescript: MockApplescript) -> None:
    """Test find with no keywords returning all contacts."""
    mock_applescript.provide("amelia", "bob", "carnival")
    result = runner.invoke(cli.app, "waldo")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_single_contact(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.provide("amelia")
    result = runner.invoke(cli.app, "amelia")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
    ]


def test_multiple_contact(mock_applescript: MockApplescript) -> None:
    """Test find with multiple contacts."""
    mock_applescript.provide("bob", "carnival")
    result = runner.invoke(cli.app, "balloon")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_multiple_keywords(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.provide("amelia", "bob")
    result = runner.invoke(cli.app, "amelia bob")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
    ]


def test_warnings(mock_applescript: MockApplescript) -> None:
    """Test reporting warnings."""
    mock_applescript.provide("warnen")
    result = runner.invoke(cli.app, "--check")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "⚠️  dr. warnen bitte sanft jr.",
    ]


def test_fix_warnings(data_path: Path, mock_applescript: MockApplescript) -> None:
    """Test fixing warnings."""
    mock_applescript.provide("warnen")
    result = runner.invoke(cli.app, "--fix")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "⚠️  dr. warnen bitte sanft jr.",
    ]
    before = Contact.read(data_path / "warnen.json")
    after = Contact.read(data_path / "warnen.fixed.json")
    diff = ContactDiff(before, after)
    assert sorted(mock_applescript._updates) == sorted(diff.updates)
    assert sorted(mock_applescript._adds) == sorted(diff.adds)
    assert sorted(mock_applescript._deletes) == sorted(diff.deletes)


def test_errors(mock_applescript: MockApplescript) -> None:
    """Test reporting errors."""
    mock_applescript.provide("errona")
    result = runner.invoke(cli.app, "--check")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "⛔ Errona Tragedia",
    ]


def test_details_single(data_path: Path, mock_applescript: MockApplescript) -> None:
    """Test detail with single contact."""
    mock_applescript.provide("amelia")
    result = runner.invoke(cli.app, "--detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = (data_path / "amelia.detail").read_text(encoding="utf-8").strip()
    assert result.stdout.strip() == expected_output


def test_details_multiple(data_path: Path, mock_applescript: MockApplescript) -> None:
    """Test detail with multiple contacts."""
    mock_applescript.provide("amelia", "bob", "carnival")
    result = runner.invoke(cli.app, "--detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = "\n".join(
        (data_path / x).with_suffix(".detail").read_text(encoding="utf-8").strip()
        for x in ["amelia", "bob", "carnival"]
    )
    assert result.stdout.strip() == expected_output


def test_details_warnings(data_path: Path, mock_applescript: MockApplescript) -> None:
    """Test warnings on detail."""
    mock_applescript.provide("warnen")
    result = runner.invoke(cli.app, "warnen --detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = (data_path / "warnen.detail").read_text(encoding="utf-8").strip()
    assert result.stdout.strip() == expected_output


def test_details_errors(data_path: Path, mock_applescript: MockApplescript) -> None:
    """Test errors on detail."""
    mock_applescript.provide("errona")
    result = runner.invoke(cli.app, "errona --detail --width=79 --no-safe-box")
    assert result.exit_code == 0
    expected_output = (data_path / "errona.detail").read_text(encoding="utf-8").strip()
    assert result.stdout.strip() == expected_output

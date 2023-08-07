"""Unittests for cli."""


import pytest
from typer.testing import CliRunner

from contacts import applescript, cli
from tests.mocks import MockApplescript

runner = CliRunner(mix_stderr=True)


@pytest.fixture(autouse=True)
def mock_applescript(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> MockApplescript:
    """Fixture for prefs."""
    mock = MockApplescript(request.path.parent / "data")
    monkeypatch.setattr(applescript, "run_and_read_output", mock.run_and_read_output)
    monkeypatch.setattr(applescript, "run_and_read_log", mock.run_and_read_log)
    return mock


def test_bare() -> None:
    """Test invocation with no arguments."""
    # TODO: #19 Bare invocation should show help. Fix when there are more commands.
    result = runner.invoke(cli.app)
    assert result.exit_code == 0
    assert not result.stdout


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


def test_find_all_contacts(mock_applescript: MockApplescript) -> None:
    """Test find with no keywords returning all contacts."""
    mock_applescript.find("amelia.json", "bob.json", "carnival.json")
    result = runner.invoke(cli.app, "waldo")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        str("👤 Amelia Avery"),
        str("   Bob Balloon"),
        str("🏢 Carnival Balloon Co."),
    ]


def test_find_single_contact(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia.json")
    result = runner.invoke(cli.app, "amelia")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        str("👤 Amelia Avery"),
    ]


def test_find_multiple_contact(mock_applescript: MockApplescript) -> None:
    """Test find with multiple contacts."""
    mock_applescript.find("bob.json", "carnival.json")
    result = runner.invoke(cli.app, "balloon")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        str("   Bob Balloon"),
        str("🏢 Carnival Balloon Co."),
    ]


def test_find_multiple_keywords(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia.json", "bob.json")
    result = runner.invoke(cli.app, "amelia bob")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        str("👤 Amelia Avery"),
        str("   Bob Balloon"),
    ]

"""Unittests for cli."""


from pathlib import Path

import pytest
from typer.testing import CliRunner

from contacts import applescript, cli
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
    monkeypatch.setattr(applescript, "run_and_read_output", mock.run_and_read_output)
    monkeypatch.setattr(applescript, "run_and_read_log", mock.run_and_read_log)
    return mock


def test_bare() -> None:
    """Test invocation with no arguments."""
    # TODO: #19 Bare invocation should show help. Fix when there are more commands.
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


def test_find_all_contacts(mock_applescript: MockApplescript) -> None:
    """Test find with no keywords returning all contacts."""
    mock_applescript.find("amelia", "bob", "carnival")
    result = runner.invoke(cli.app, "waldo")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_find_single_contact(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia")
    result = runner.invoke(cli.app, "amelia")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
    ]


def test_find_multiple_contact(mock_applescript: MockApplescript) -> None:
    """Test find with multiple contacts."""
    mock_applescript.find("bob", "carnival")
    result = runner.invoke(cli.app, "balloon")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_find_multiple_keywords(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia", "bob")
    result = runner.invoke(cli.app, "amelia bob")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
    ]


def test_find_details_single(
    data_path: Path, mock_applescript: MockApplescript
) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia")
    result = runner.invoke(cli.app, "--detail --no-safe-box")
    assert result.exit_code == 0
    expected_output = (data_path / "amelia.detail").read_text(encoding="utf-8").strip()
    assert result.stdout.strip() == expected_output


def test_find_details_multiple(
    data_path: Path, mock_applescript: MockApplescript
) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia", "bob", "carnival")
    result = runner.invoke(cli.app, "--detail --no-safe-box")
    assert result.exit_code == 0
    expected_output = "\n".join(
        (data_path / x).with_suffix(".detail").read_text(encoding="utf-8").strip()
        for x in ["amelia", "bob", "carnival"]
    )
    assert result.stdout.strip() == expected_output

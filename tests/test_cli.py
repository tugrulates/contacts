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
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_find_single_contact(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia.json")
    result = runner.invoke(cli.app, "amelia")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
    ]


def test_find_multiple_contact(mock_applescript: MockApplescript) -> None:
    """Test find with multiple contacts."""
    mock_applescript.find("bob.json", "carnival.json")
    result = runner.invoke(cli.app, "balloon")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Bob Balloon",
        "🏢 Carnival Balloon Co.",
    ]


def test_find_multiple_keywords(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia.json", "bob.json")
    result = runner.invoke(cli.app, "amelia bob")
    assert result.exit_code == 0
    assert result.stdout.rstrip().split("\n") == [
        "👤 Ms. Amelia Avery Arch.",
        "👤 Bob Balloon",
    ]


def test_find_details(mock_applescript: MockApplescript) -> None:
    """Test find with single contact."""
    mock_applescript.find("amelia.json", "bob.json", "carnival.json")
    result = runner.invoke(cli.app, "--detail --no-safe-box")
    assert result.exit_code == 0
    assert [x for x in result.stdout.split("\n") if x.strip()] == [
        "╭──────────────────────┬────────────────────────────╮",
        "│                      │ 👤 Ms. Amelia Avery Arch.  │",
        "├──────────────────────┼────────────────────────────┤",
        "│             Nickname │ 🔖 Amelie                  │",
        "│               Prefix │ 🔖 Ms.                     │",
        "│           First name │ 🔖 Amelia                  │",
        "│          Middle name │ 🔖 Ada                     │",
        "│            Last name │ 🔖 Avery                   │",
        "│               Suffix │ 🔖 Arch.                   │",
        "│          Maiden name │ 🔖 Anglais                 │",
        "│  Phonetic first name │ 🎧 a-mel-ia                │",
        "│ Phonetic middle name │ 🎧 AY-duh                  │",
        "│   Phonetic last name │ 🎧 AYV-ree                 │",
        "│         Organization │ 💼 Avery & Avery           │",
        "│           Department │ 💼 Administrative          │",
        "│            Job title │ 💼 Architect               │",
        "│               Phones │ 📱 +11111111111            │",
        "│                      │ 💼 +11111111112            │",
        "│               Emails │ 🏠 amelia@avery.com        │",
        "│            Home page │ 🌐 https://www.avery.com   │",
        "│                 Urls │ 🏠 https://www.avery.com   │",
        "│      Social profiles │ 🌐 amelie (Duolingo)       │",
        "│                      │ 🌐 AmeliaAvery (LinkedIn)  │",
        "│     Instant messages │ 💬 +11111111111 (WhatsApp) │",
        "│                      │ 💬 1111111 (ICQ)           │",
        "│            Addresses │ 🏠 111 Arlington Blvd      │",
        "│                      │    Arlington, TX 76010     │",
        "│                      │    United States           │",
        "│                      │ 📫 1 Arlington Blvd        │",
        "│                      │    P.O. Box 11             │",
        "│                      │    Arlington, TX 76010     │",
        "│                      │    United States           │",
        "│           Birth date │ 📅 January 1, 2001         │",
        "│         Custom dates │ 💍 November 11             │",
        "│                      │ 📅 November 11, 2011       │",
        "│        Related names │ 👥 Bob Balloon             │",
        "│                 Note │ 📋 A trusted contact.      │",
        "╰──────────────────────┴────────────────────────────╯",
        "╭──────────────────────┬──────────────────╮",
        "│                      │ 👤 Bob Balloon   │",
        "├──────────────────────┼──────────────────┤",
        "│           First name │ 🔖 Bob           │",
        "│          Middle name │ 🔖 Babála        │",
        "│            Last name │ 🔖 Balon         │",
        "│            Job title │ 💼 Baker         │",
        "│               Phones │ 📱 +222222222222 │",
        "╰──────────────────────┴──────────────────╯",
        "╭──────────────────────┬──────────────────────────────╮",
        "│                      │ 🏢 Carnival Balloon Co.      │",
        "├──────────────────────┼──────────────────────────────┤",
        "│               Phones │ 📱 +3333333333333            │",
        "│               Emails │ 💼 order@carnivalballoon.com │",
        "│                      │ 💼 order@carnivalballoon.com │",
        "╰──────────────────────┴──────────────────────────────╯",
    ]

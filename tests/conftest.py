"""Common test configuration."""

import importlib
from pathlib import Path

import email_validator
import pytest

from contacts import address, address_book, checks, config
from contacts.checks import url_check
from tests.mocks import MockAddressBook, MockGeocoder


@pytest.fixture(scope="session", autouse=True)
def environment() -> None:
    """Initialize the test environment."""
    # disable DNS checks for e-mail address and URL checks
    email_validator.TEST_ENVIRONMENT = True
    url_check.TEST_ENVIRONMENT = True


@pytest.fixture(autouse=True)
def data_path(request: pytest.FixtureRequest) -> Path:
    """Fixture for the test data directory."""
    return request.path.parent / "data"  # type: ignore


@pytest.fixture(autouse=True)
def mock_config(monkeypatch: pytest.MonkeyPatch) -> config.Config:
    """Fixture for mock configuration."""
    mock = config.Config()
    monkeypatch.setattr(config, "get_config", lambda *args, **kwargs: mock)
    return mock


@pytest.fixture(autouse=True)
def mock_address_book(
    monkeypatch: pytest.MonkeyPatch, data_path: Path
) -> MockAddressBook:
    """Fixture for mock address book."""
    mock = MockAddressBook(data_path)
    monkeypatch.setattr(address_book, "get_address_book", lambda *args, **kwargs: mock)
    return mock


@pytest.fixture(autouse=True)
def mock_geocoder(monkeypatch: pytest.MonkeyPatch) -> MockGeocoder:
    """Fixture for mock geocoder."""
    mock = MockGeocoder()
    monkeypatch.setattr(address, "get_geocoder", lambda *args, **kwargs: mock)
    importlib.reload(checks)
    return mock

"""MockAddressBook class."""


import json
from pathlib import Path
from typing import Iterator

from contacts.address_book import AddressBook
from contacts.contact import Contact
from tests.contact_diff import Mutation


class MockAddressBook(AddressBook):
    """Mock object for manipulation contacts."""

    def __init__(self, test_data_path: Path):
        """Initialize the mock."""
        self._test_data_path = test_data_path
        self._error = False
        self._data: dict[str, Contact] = {}
        self.updates: list[Mutation] = []
        self.adds: list[Mutation] = []
        self.deletes: list[Mutation] = []

    def error(self) -> None:
        """Raise an error upon invocation."""
        self._error = True

    def provide(self, *find_data: str) -> None:
        """Specify which test data to find in contacts."""
        contacts = [
            Contact(
                **json.loads(
                    Path(self._test_data_path / x)
                    .with_suffix(".json")
                    .read_text(encoding="utf-8")
                )
            )
            for x in find_data
        ]
        self._data = {x.id: x for x in contacts}

    def count(self, _: list[str]) -> int:
        """Return number of contacts matching given keywords."""
        if self._error:
            raise RuntimeError(1, "count")
        return len(self._data)

    def find(self, _: list[str]) -> Iterator[Contact]:
        """Return list of contact ids matching given keywords."""
        if self._error:
            raise RuntimeError(1, "find")
        yield from self._data.values()

    def get(self, contact_id: str) -> Contact:
        """Fetch a contact with its id."""
        if self._error:
            raise RuntimeError(1, "get")
        return self._data[contact_id]

    def _update_field(self, contact_id: str, field: str, value: str) -> None:
        """Update a contact field with given value."""
        self.updates.append((contact_id, field, value))

    def _delete_field(self, contact_id: str, field: str) -> None:
        """Delete a contact field."""
        self.deletes.append((contact_id, field))

    def _update_info(
        self, contact_id: str, field: str, info_id: str, **values: str
    ) -> None:
        """Update a contact info with given label and value."""
        self.updates.append((contact_id, field, info_id, values))

    def _add_info(self, contact_id: str, field: str, **values: str) -> None:
        """Add a contact info."""
        self.adds.append((contact_id, field, values))

    def _delete_info(self, contact_id: str, field: str, info_id: str) -> None:
        """Delete a contact info."""
        self.deletes.append((contact_id, field, info_id))

"""AddressBook abstract base class."""


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from contacts import contact


class AddressBook(ABC):
    """An address book that fetches and updates contacts."""

    @abstractmethod
    def count(self, keywords: list[str]) -> int:
        """Return number of contacts matching given keywords."""

    @abstractmethod
    def find(self, keywords: list[str]) -> Iterator[contact.Contact]:
        """Return list of contact ids matching given keywords."""

    @abstractmethod
    def get(self, contact_id: str) -> contact.Contact:
        """Fetch a contact with its id."""

    @abstractmethod
    def update_field(self, contact_id: str, field: str, value: str) -> None:
        """Update a contact field with given value."""

    @abstractmethod
    def delete_field(self, contact_id: str, field: str) -> None:
        """Delete a contact field."""

    @abstractmethod
    def update_info(
        self, contact_id: str, field: str, info_id: str, label: str, value: str
    ) -> None:
        """Update a contact info with given label and value."""

    @abstractmethod
    def add_info(self, contact_id: str, field: str, label: str, value: str) -> None:
        """Add a contact info."""

    @abstractmethod
    def delete_info(self, contact_id: str, field: str, info_id: str) -> None:
        """Delete a contact info."""

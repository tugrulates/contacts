"""Contact operations."""

import json
from typing import Any, Iterator, Sequence

from contacts import applescript


class Contact:
    """A single contact person or company."""

    def __init__(self, data: dict[str, Any]):
        """Initialize contact from query output."""
        self._data = data

    @property
    def identifier(self) -> str:
        """Return the id of this contact."""
        return str(self._data["id"])

    @property
    def name(self) -> str:
        """Return the full name of this contact."""
        return str(self._data["name"])

    @property
    def has_image(self) -> bool:
        """Return whether this contact has an image."""
        return bool(self._data["has_image"])

    @property
    def is_company(self) -> bool:
        """Return whether this contact is a company."""
        return bool(self._data["is_company"])

    def __str__(self) -> str:
        """Full name of contact."""
        return f"{self.name}"

    def __repr__(self) -> str:
        """Contact object repr."""
        return f"Contact({self.name})"


def by_keyword(keywords: Sequence[str]) -> Iterator[Contact]:
    """Find contacts matching given keyword."""
    for contact_id in applescript.run_and_read_log("find", *keywords):
        yield by_id(contact_id)


def by_id(contact_id: str) -> Contact:
    """Create contact by id."""
    return Contact(json.loads(applescript.run_and_read_output("detail", contact_id)))

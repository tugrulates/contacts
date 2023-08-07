"""Contact operations."""

import json
from itertools import zip_longest
from typing import Any, Iterator

from contacts import applescript

BATCH_DETAIL_SIZE = 10


class Contact:
    """A single contact person or company."""

    def __init__(self, data: dict[str, Any]):
        """Initialize contact from query output."""
        self._data = data

    @property
    def contact_id(self) -> str:
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


def by_keyword(*keywords: str) -> Iterator[Contact]:
    """Find contacts matching given keyword."""
    contact_ids = applescript.run_and_read_log("find", *keywords)
    chunks = zip_longest(*([iter(contact_ids)] * BATCH_DETAIL_SIZE))
    for chunk in chunks:
        yield from by_id(*(x for x in chunk if x))


def by_id(*contact_ids: str) -> Iterator[Contact]:
    """Create contact by id."""
    result = json.loads(applescript.run_and_read_output("detail", *contact_ids))
    for contact in result:
        yield Contact(contact)

"""Contact operations."""

from typing import Any

import yaml

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


def find(keywords: list[str]) -> list[Contact]:
    """Find contacts matching given keyword."""
    result = yaml.safe_load(applescript.run("find", *keywords))
    return [Contact(x) for x in result]

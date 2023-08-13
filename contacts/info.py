"""Info class."""


import abc
from typing import Any

from contacts.category import Category


class Info(metaclass=abc.ABCMeta):
    """A single information with a category."""

    @property
    @abc.abstractmethod
    def category(self) -> Category:
        """Return the category of this info."""

    @property
    @abc.abstractmethod
    def value(self) -> str:
        """Return the value of this info."""

    def __str__(self) -> str:
        """Convert info to string."""
        value_str = self.value.replace("\n", "\n   ")
        icon_padding = " " * len(self.category.icon)
        return f"{self.category.icon}{icon_padding}{value_str}"

    def __repr__(self) -> str:
        """Info object repr."""
        return f"{type(self)}({self.value})"


class SimpleInfo(Info):
    """A single info with an icon."""

    def __init__(self, category: Category, value: str):
        """Initialize info from query output."""
        self._category = category
        self._value = value

    @property
    def category(self) -> Category:
        """Return the category of this info."""
        return self._category

    @property
    def value(self) -> str:
        """Return the value of this info."""
        return self._value


class ContactInfo(Info):
    """An multi-value info with an id.

    Corresponds to a "contact info" on AppleScript.

    The data will have the following properties:
      - id: id of the property, different from contact id
      - label: label of the property, used to determine category
      - value: actual value of the property
    """

    def __init__(self, category: Category, data: dict[str, Any]):
        """Initialize info from query output."""
        self._category = category
        self._data = data

    @property
    def info_id(self) -> str:
        """Return the id of this info."""
        return str(self._data["id"])

    @property
    def category(self) -> Category:
        """Return the category of this info."""
        return Category.from_label(self.label, self._category)

    @property
    def label(self) -> str:
        """Return the label of this info."""
        return str(self._data["label"])

    @property
    def value(self) -> str:
        """Return the value of this info."""
        return str(self._data["value"])

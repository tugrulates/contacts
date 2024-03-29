"""Problem checks."""

from __future__ import annotations

import abc
from typing import Any, Callable, Optional

from contacts import address_book, contact
from contacts.category import Category


class Check(metaclass=abc.ABCMeta):
    """A single problem check."""

    @abc.abstractmethod
    def check(self, contact: contact.Contact) -> list[Problem]:
        """Check contact."""


class Problem:
    """Represents something being off in a contact."""

    def __init__(
        self,
        message: str,
        fix: Optional[Callable[[address_book.AddressBook], Any]] = None,
    ):
        """Initialize problem details."""
        self.message = message.replace("\n", " ")
        self.fix = fix

    @property
    def category(self) -> Category:
        """Return the category of this problem."""
        return Category.WARNING if self.fix else Category.ERROR

    def try_fix(self, address_book: address_book.AddressBook) -> None:
        """Attempt to fix this problem."""
        if self.fix:
            self.fix(address_book)

    def __repr__(self) -> str:
        """Return problem representation."""
        return f"Problem({self.message}, {self.fix})"

"""Problem checks."""


from __future__ import annotations

import abc
from typing import Any, Callable, Optional

from contacts import contact
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
        fix: Optional[Callable[[], Any]] = None,
    ):
        """Initialize problem details."""
        self.message = message
        self.fix = fix

    @property
    def category(self) -> Category:
        """Return the category of this problem."""
        return Category.WARNING if self.fix else Category.ERROR

    def try_fix(self) -> None:
        """Attempt to fix this problem."""
        if self.fix:
            self.fix()


def find_problems(contact: contact.Contact) -> list[Problem]:
    """Return all problems in a given contact."""
    from contacts.checks import Checks

    problems = []
    for check in Checks:
        problems.extend(check.value.check(contact))
    return problems

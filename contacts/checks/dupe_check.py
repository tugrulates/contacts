"""DupeCheck class."""


from __future__ import annotations

from itertools import groupby
from typing import Iterator, Optional

from contacts.address_book import AddressBook
from contacts.contact import Contact, ContactInfo
from contacts.field import ContactInfoMetadata
from contacts.problem import Check, Problem


class DupeCheck(Check):
    """Checker for duplicate contact info."""

    def __init__(self, field: ContactInfoMetadata, with_label: bool):
        """Initialize checker for an info field."""
        self.field = field
        self.with_label = with_label

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def key(info: ContactInfo) -> tuple[str, ...]:
            return (info.value, info.label) if self.with_label else (info.value,)

        def check_group(
            group: Iterator[ContactInfo],
        ) -> Optional[Problem]:
            duplicates = list(group)
            if len(duplicates) == 1:
                return None

            def fix(address_book: AddressBook) -> None:
                for duplicate in duplicates[1:]:
                    self.field.delete(address_book, contact.id, duplicate.id)

            return Problem(
                f"{self.field.singular} '{duplicates[0]}' has duplicate(s).",
                fix=fix,
            )

        problems = []
        infos = sorted(self.field.get(contact), key=key)
        for _, group in groupby(infos, key=key):
            problem = check_group(group)
            if problem:
                problems.append(problem)
        return problems

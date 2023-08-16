"""Enforces a standard phone format."""


from __future__ import annotations

from typing import Optional

from contacts.address_book import AddressBook
from contacts.contact import Contact
from contacts.problem import Check, Problem


class CapitalizationCheck(Check):
    """Checker for capitalization of names."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_name(field: str, name: Optional[str]) -> Optional[Problem]:
            metadata = Contact.metadata(field)
            if not metadata:
                return None

            # if all letters are lowercase, capitalize first word only
            if name is None or name.lower() != name:
                return None
            if name == name.capitalize():
                return None

            def fix(address_book: AddressBook) -> None:
                if name:
                    address_book.update_field(
                        contact.contact_id, field, name.capitalize()
                    )

            return Problem(
                f"{metadata.singular} '{name}' should be '{name.capitalize()}'.",
                fix=fix,
            )

        problems = [
            check_name("prefix", contact.prefix),
            check_name("first_name", contact.first_name),
            check_name("middle_name", contact.middle_name),
            check_name("last_name", contact.last_name),
            check_name("maiden_name", contact.maiden_name),
            check_name("suffix", contact.suffix),
            check_name("nickname", contact.nickname),
            check_name("job_title", contact.job_title),
            check_name("department", contact.department),
        ]
        return [x for x in problems if x]

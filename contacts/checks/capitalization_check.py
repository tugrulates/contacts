"""Enforces a standard phone format."""


from __future__ import annotations

from typing import Callable, Optional

from contacts import address_book
from contacts.contact import Contact
from contacts.problem import Check, Problem


class CapitalizationCheck(Check):
    """Checker for capitalization of names."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_name(
            field: str, name: Optional[str], fix: Callable[[Contact, str], str]
        ) -> Optional[Problem]:
            # if all letters are lowercase, capitalize first word only
            if not name or name.lower() != name:
                return None
            if name != name.capitalize():
                return Problem(
                    f"{field} '{name}' should be '{name.capitalize()}'.",
                    fix=lambda: fix(contact, name.capitalize()) if name else None,
                )
            return None

        problems = [
            check_name(
                "Prefix",
                contact.prefix,
                address_book.update_prefix,
            ),
            check_name(
                "First name",
                contact.first_name,
                address_book.update_first_name,
            ),
            check_name(
                "Middle name",
                contact.middle_name,
                address_book.update_middle_name,
            ),
            check_name(
                "Last name",
                contact.last_name,
                address_book.update_last_name,
            ),
            check_name(
                "Maiden name",
                contact.maiden_name,
                address_book.update_maiden_name,
            ),
            check_name(
                "Suffix",
                contact.suffix,
                address_book.update_suffix,
            ),
            check_name(
                "Nickname",
                contact.nickname,
                address_book.update_nickname,
            ),
            check_name(
                "Job title",
                contact.job_title,
                address_book.update_job_title,
            ),
            check_name(
                "Department",
                contact.department,
                address_book.update_department,
            ),
        ]
        return [x for x in problems if x]

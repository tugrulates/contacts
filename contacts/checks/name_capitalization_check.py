"""Enforces a standard phone format."""


from __future__ import annotations

from typing import Callable, Optional

from contacts import address_book
from contacts.contact import Contact
from contacts.problem import Check, Problem


class NameCapitalizationCheck(Check):
    """Checker for capitalization of names."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def _(
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
            _("Prefix", contact.prefix, address_book.update_prefix),
            _("First name", contact.first_name, address_book.update_first_name),
            _("Middle name", contact.middle_name, address_book.update_middle_name),
            _("Last name", contact.last_name, address_book.update_last_name),
            _("Maiden name", contact.maiden_name, address_book.update_maiden_name),
            _("Suffix", contact.suffix, address_book.update_suffix),
            _("Nickname", contact.nickname, address_book.update_nickname),
            _("Job title", contact.job_title, address_book.update_job_title),
            _("Department", contact.department, address_book.update_department),
        ]
        return [x for x in problems if x]

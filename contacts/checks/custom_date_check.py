"""Enforces a standard phone format."""


from __future__ import annotations

from typing import Optional

from contacts.address_book import AddressBook
from contacts.category import Category
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class CustomDateCheck(Check):
    """Checker for custom dates."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_label(custom_date: ContactInfo) -> Optional[Problem]:
            if Category.from_label(custom_date.label) is not None:
                return None

            formatted = custom_date.label.lower()
            if custom_date.value == formatted:
                return None

            def fix(address_book: AddressBook) -> None:
                address_book.update_info(
                    contact.contact_id,
                    "custom_dates",
                    custom_date.info_id,
                    label=formatted,
                )

            return Problem(
                f"Custom date label <{custom_date.label}> should be <{formatted}>.",
                fix=fix,
            )

        problems = [check_label(custom_date) for custom_date in contact.custom_dates]
        return [x for x in problems if x]

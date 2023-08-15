"""Enforces a standard phone format."""


from __future__ import annotations

from typing import Optional

import phonenumbers

from contacts import address_book
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class PhoneCheck(Check):
    """Checker for phone numbers."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_format(phone: ContactInfo) -> Optional[Problem]:
            try:
                formatted = phonenumbers.format_number(
                    phonenumbers.parse(phone.value),
                    phonenumbers.PhoneNumberFormat.E164,
                )
            except phonenumbers.NumberParseException:
                return Problem(f"Phone number '{phone.value}' is not valid.")
            if phone.value == formatted:
                return None
            return Problem(
                f"Phone number '{phone.value}' should be formatted as '{formatted}'.",
                fix=lambda: address_book.update_phone(
                    contact, phone, phone.label, formatted
                ),
            )

        problems = [check_format(phone) for phone in contact.phones]
        return [x for x in problems if x]

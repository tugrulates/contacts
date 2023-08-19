"""PhoneCheck class."""


from __future__ import annotations

from functools import partial
from typing import Optional

import phonenumbers

from contacts.address_book import AddressBook
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class PhoneCheck(Check):
    """Checker for phone numbers."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_value(phone: ContactInfo) -> Optional[Problem]:
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
                f"Phone number '{phone.value}' should be '{formatted}'.",
                fix=partial(
                    AddressBook.update_phone,
                    contact_id=contact.contact_id,
                    info_id=phone.info_id,
                    value=formatted,
                ),
            )

        problems = [check_value(phone) for phone in contact.phones]
        return [x for x in problems if x]

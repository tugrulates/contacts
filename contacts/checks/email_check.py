"""EmailCheck class."""

from __future__ import annotations

from functools import partial
from typing import Optional

from email_validator import EmailNotValidError, validate_email

from contacts.address_book import AddressBook
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class EmailCheck(Check):
    """Checker for e-mail addresses."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_value(email: ContactInfo) -> Optional[Problem]:
            try:
                formatted = validate_email(
                    email.value.strip(), check_deliverability=True
                ).normalized
            except EmailNotValidError:
                return Problem(f"E-mail '{email.value}' is not valid.")
            if email.value == formatted:
                return None

            return Problem(
                f"E-mail '{email.value}' should be '{formatted}'.",
                fix=partial(
                    AddressBook.update_email,
                    contact_id=contact.id,
                    info_id=email.id,
                    value=formatted,
                ),
            )

        problems = (check_value(email) for email in contact.emails)
        return [x for x in problems if x]

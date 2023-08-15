"""Enforces a standard phone format."""


from __future__ import annotations

from typing import Optional

from email_validator import EmailNotValidError, validate_email

from contacts import address_book
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class EmailCheck(Check):
    """Checker for e-mail addresses."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_format(email: ContactInfo) -> Optional[Problem]:
            try:
                formatted = validate_email(
                    email.value.strip(),
                    allow_quoted_local=True,
                    check_deliverability=True,
                ).normalized
            except EmailNotValidError:
                return Problem(f"E-mail '{email.value}' is not valid.")
            if email.value == formatted:
                return None
            return Problem(
                f"E-mail '{email.value}' should be formatted as '{formatted}'.",
                fix=lambda: address_book.update_email(
                    contact, email, email.label, formatted
                ),
            )

        problems = [check_format(email) for email in contact.emails]
        return [x for x in problems if x]

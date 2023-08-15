"""Enforces a standard phone format."""


from __future__ import annotations

from typing import Optional

from contacts import address_book
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class UrlCheck(Check):
    """Checker for URLs."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_label(url: ContactInfo) -> Optional[Problem]:
            if url.label != "_$!<Home>!$_":
                return None
            return Problem(
                f"URL '{url.value}' should have a <HomePage> label.",
                fix=lambda: address_book.update_url(
                    contact, url, "_$!<HomePage>!$_", url.value
                ),
            )

        problems = [check_label(url) for url in contact.urls]
        return [x for x in problems if x]

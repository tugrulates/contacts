"""Enforces a standard phone format."""


from __future__ import annotations

from contacts import address_book
from contacts.contact import Contact
from contacts.problem import Check, Problem


class HomePageCheck(Check):
    """Checker for home page, which should be a URL instead."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def fix(contact: Contact) -> None:
            """Replace home page with a URL."""
            if contact.home_page:
                address_book.add_url(contact, "_$!<HomePage>!$_", contact.home_page)
                address_book.delete_home_page(contact)

        if contact.home_page:
            return [
                Problem(
                    f"Home page '{contact.home_page}' should be a URL.",
                    fix=lambda: fix(contact),
                )
            ]
        return []

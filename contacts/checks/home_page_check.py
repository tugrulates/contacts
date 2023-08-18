"""HomePageCheck class."""


from __future__ import annotations

from contacts.address_book import AddressBook
from contacts.contact import Contact
from contacts.problem import Check, Problem


class HomePageCheck(Check):
    """Checker for home page, which should be a URL instead."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def fix(address_book: AddressBook) -> None:
            """Replace home page with a URL."""
            if contact.home_page:
                address_book.add_info(
                    contact.contact_id,
                    "urls",
                    label="_$!<HomePage>!$_",
                    value=contact.home_page,
                )
                address_book.delete_field(contact.contact_id, "home_page")

        if contact.home_page:
            return [
                Problem(
                    f"Home page '{contact.home_page}' should be a URL.",
                    fix=fix,
                )
            ]
        return []

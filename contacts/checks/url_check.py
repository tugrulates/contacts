"""UrlCheck class."""


from __future__ import annotations

import socket
from itertools import chain
from typing import Optional
from urllib.parse import unwrap, urlparse

from contacts.address_book import AddressBook
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem

TEST_ENVIRONMENT = False


class UrlCheck(Check):
    """Checker for URLs."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_label(url: ContactInfo) -> Optional[Problem]:
            if url.label != "_$!<Home>!$_":
                return None

            def fix(address_book: AddressBook) -> None:
                address_book.update_info(
                    contact.contact_id,
                    "urls",
                    url.info_id,
                    label="_$!<HomePage>!$_",
                )

            return Problem(
                f"URL '{url.value}' should have a <HomePage> label.",
                fix=fix,
            )

        def check_value(url: ContactInfo) -> Optional[Problem]:
            parsed = urlparse(unwrap(url.value.strip()))
            formatted = parsed.geturl()

            if not (parsed.scheme and parsed.hostname):
                return Problem(f"URL '{url.value}' is not valid.")
            try:
                if not TEST_ENVIRONMENT:
                    socket.getaddrinfo(parsed.hostname, parsed.port)
            except socket.gaierror:
                return Problem(f"URL '{url.value}' is not reachable.")

            if url.value == formatted:
                return None

            def fix(address_book: AddressBook) -> None:
                address_book.update_info(
                    contact.contact_id, "urls", url.info_id, value=formatted
                )

            return Problem(
                f"URL '{url.value}' should be '{formatted}'.",
                fix=fix,
            )

        problems = chain(
            [check_label(url) for url in contact.urls],
            [check_value(url) for url in contact.urls],
        )
        return [x for x in problems if x]

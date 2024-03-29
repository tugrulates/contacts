"""UrlCheck class."""

from __future__ import annotations

import socket
from functools import partial
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

            return Problem(
                f"URL label for '{url.value}' should be <HomePage>.",
                fix=partial(
                    AddressBook.update_url,
                    contact_id=contact.id,
                    info_id=url.id,
                    label="_$!<HomePage>!$_",
                ),
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

            return Problem(
                f"URL '{url.value}' should be '{formatted}'.",
                fix=partial(
                    AddressBook.update_url,
                    contact_id=contact.id,
                    info_id=url.id,
                    value=formatted,
                ),
            )

        problems = chain(
            [check_label(url) for url in contact.urls],
            [check_value(url) for url in contact.urls],
        )
        return [x for x in problems if x]

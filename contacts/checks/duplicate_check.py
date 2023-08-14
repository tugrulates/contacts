"""Enforces a standard phone format."""


from __future__ import annotations

from itertools import chain, groupby
from typing import Callable, Iterator, Optional, Sequence

from contacts import address_book
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class DuplicateCheck(Check):
    """Checker for duplicate contact info."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_infos(
            field: str,
            with_label: bool,
            infos: Sequence[ContactInfo],
            fix: Callable[[Contact, ContactInfo], str],
        ) -> list[Optional[Problem]]:
            def key(info: ContactInfo) -> tuple[str, ...]:
                return (info.value, info.label) if with_label else (info.value,)

            problems = []
            infos = sorted(infos, key=key)
            for _, group in groupby(infos, key=key):
                problems.append(check_group(field, group, fix))
            return problems

        def check_group(
            field: str,
            group: Iterator[ContactInfo],
            fix: Callable[[Contact, ContactInfo], str],
        ) -> Optional[Problem]:
            duplicates = list(group)[1:]
            if duplicates:
                return Problem(
                    f"{field} '{duplicates[0]}' has duplicate(s).",
                    fix=lambda: [fix(contact, x) for x in duplicates],
                )
            return None

        problems = chain(
            check_infos(
                "Phone",
                False,
                contact.phones,
                address_book.delete_phone,
            ),
            check_infos(
                "Email",
                False,
                contact.emails,
                address_book.delete_email,
            ),
            check_infos(
                "URL",
                False,
                contact.urls,
                address_book.delete_url,
            ),
            check_infos(
                "Address",
                False,
                contact.addresses,
                address_book.delete_address,
            ),
            check_infos(
                "Custom date",
                True,
                contact.custom_dates,
                address_book.delete_custom_date,
            ),
            check_infos(
                "Social profile",
                True,
                contact.social_profiles,
                address_book.delete_social_profile,
            ),
            check_infos(
                "Instant message",
                True,
                contact.instant_messages,
                address_book.delete_instant_message,
            ),
        )
        return [x for x in problems if x]

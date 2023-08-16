"""Enforces a standard phone format."""


from __future__ import annotations

from itertools import chain, groupby
from typing import Iterator, Optional, Sequence

from contacts.address_book import AddressBook
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem


class DuplicateCheck(Check):
    """Checker for duplicate contact info."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_infos(
            field: str, with_label: bool, infos: Sequence[ContactInfo]
        ) -> list[Optional[Problem]]:
            def key(info: ContactInfo) -> tuple[str, ...]:
                return (info.value, info.label) if with_label else (info.value,)

            problems = []
            infos = sorted(infos, key=key)
            for _, group in groupby(infos, key=key):
                problems.append(check_group(field, group))
            return problems

        def check_group(
            field: str,
            group: Iterator[ContactInfo],
        ) -> Optional[Problem]:
            metadata = Contact.metadata(field)
            if not metadata:
                return None

            duplicates = list(group)[1:]
            if not duplicates:
                return None

            def fix(address_book: AddressBook) -> None:
                for duplicate in duplicates:
                    address_book.delete_info(
                        contact.contact_id, field, duplicate.info_id
                    )

            return Problem(
                f"{metadata.singular} '{duplicates[0]}' has duplicate(s).",
                fix=fix,
            )

        problems = chain(
            check_infos("phones", False, contact.phones),
            check_infos("emails", False, contact.emails),
            check_infos("urls", False, contact.urls),
            check_infos("addresses", False, contact.addresses),
            check_infos("custom_dates", True, contact.custom_dates),
            check_infos("social_profiles", True, contact.social_profiles),
            check_infos("instant_messages", True, contact.instant_messages),
        )
        return [x for x in problems if x]

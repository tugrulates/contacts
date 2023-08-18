"""Enforces a standard phone format."""


from __future__ import annotations

from itertools import chain
from typing import Optional

from contacts.address_book import AddressBook
from contacts.category import Category
from contacts.contact import Contact, ContactInfo
from contacts.problem import Check, Problem

FIXABLE: dict[tuple[Optional[str], str], str] = {
    ("phones", "mobile"): "_$!<Mobile>!$_",
    ("phones", "mobil"): "_$!<Mobile>!$_",
    ("phones", "cep telefonu"): "_$!<Mobile>!$_",
    ("emails", "email"): "_$!<Home>!$_",
    ("urls", "home"): "_$!<HomePage>!$_",
    (None, "home"): "_$!<Home>!$_",
    (None, "ev"): "_$!<Home>!$_",
    (None, "work"): "_$!<Work>!$_",
    (None, "iş"): "_$!<Work>!$_",
    (None, "school"): "_$!<School>!$_",
    (None, "okul"): "_$!<School>!$_",
}


class LabelCheck(Check):
    """Checker for invalid labels."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_info(field: str, info: ContactInfo) -> Optional[Problem]:
            metadata = Contact.metadata(field)
            if not metadata:
                return None

            if Category.from_label(info.label):
                return None

            corrected = FIXABLE.get(
                (field, info.label.lower()), FIXABLE.get((None, info.label.lower()))
            )

            if not corrected:
                return Problem(
                    f"{metadata.singular} label <{info.label}> is not valid."
                )

            def fix(address_book: AddressBook) -> None:
                if corrected:
                    address_book.update_info(
                        contact.contact_id,
                        field,
                        info.info_id,
                        label=corrected,
                    )

            return Problem(
                f"{metadata.singular} label <{info.label}> should be <{corrected}>.",
                fix=fix,
            )

        problems = chain(
            (check_info("phones", x) for x in contact.phones),
            (check_info("emails", x) for x in contact.emails),
            (check_info("urls", x) for x in contact.urls),
            (check_info("addresses", x) for x in contact.addresses),
        )
        return [x for x in problems if x]

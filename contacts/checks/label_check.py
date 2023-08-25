"""LabelCheck class."""


from __future__ import annotations

from functools import partial
from typing import Optional

from contacts.category import Category
from contacts.contact import Contact, ContactInfo
from contacts.field import ContactFields, ContactInfoMetadata
from contacts.problem import Check, Problem

FIXABLE: dict[tuple[Optional[ContactInfoMetadata], str], str] = {
    (ContactFields.PHONE.value, "mobile"): "_$!<Mobile>!$_",
    (ContactFields.PHONE.value, "mobil"): "_$!<Mobile>!$_",
    (ContactFields.PHONE.value, "cep telefonu"): "_$!<Mobile>!$_",
    (ContactFields.EMAIL.value, "email"): "_$!<Home>!$_",
    (ContactFields.URL.value, "home"): "_$!<HomePage>!$_",
    (None, "home"): "_$!<Home>!$_",
    (None, "ev"): "_$!<Home>!$_",
    (None, "work"): "_$!<Work>!$_",
    (None, "iş"): "_$!<Work>!$_",
    (None, "school"): "_$!<School>!$_",
    (None, "okul"): "_$!<School>!$_",
}


class LabelCheck(Check):
    """Checker for invalid labels."""

    def __init__(self, field: ContactInfoMetadata):
        """Initialize checker for an info field."""
        self.field = field

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def check_label(info: ContactInfo) -> Optional[Problem]:
            if Category.from_label(info.label):
                return None

            corrected = FIXABLE.get(
                (self.field, info.label.lower()),
                FIXABLE.get((None, info.label.lower())),
            )

            if not corrected:
                return Problem(
                    f"{self.field.singular} label <{info.label}> is not valid."
                )

            return Problem(
                f"{self.field.singular} label <{info.label}> should be <{corrected}>.",
                fix=partial(
                    self.field.update,
                    contact_id=contact.id,
                    info_id=info.id,
                    label=corrected,
                ),
            )

        problems = [check_label(info) for info in self.field.get(contact)]
        return [x for x in problems if x]

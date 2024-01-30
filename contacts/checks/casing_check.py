"""CasingCheck class."""

from __future__ import annotations

from functools import partial

from contacts.contact import Contact
from contacts.field import ContactFieldMetadata
from contacts.problem import Check, Problem


class CasingCheck(Check):
    """Checker for casing of names."""

    def __init__(self, field: ContactFieldMetadata):
        """Initialize checker for a name field."""
        self.field = field

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""
        name = self.field.get(contact)

        # if all letters are lowercase, capitalize first word only
        if name is None or name.lower() != name:
            return []
        if name == name.capitalize():
            return []

        return [
            Problem(
                f"{self.field.singular} '{name}' should be '{name.capitalize()}'.",
                fix=partial(
                    self.field.update,
                    contact_id=contact.id,
                    value=name.capitalize(),
                ),
            )
        ]

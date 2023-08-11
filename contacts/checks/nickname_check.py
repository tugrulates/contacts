"""Enforces a standard phone format."""


from __future__ import annotations

from contacts.contact import Contact
from contacts.problem import Check, Problem


class NicknameCheck(Check):
    """Checker for nicknames."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""
        if contact.nickname and len(contact.nickname.value.split()) == 1:
            return [Problem(f"Nickname {contact.nickname} is not a full name.")]
        return []

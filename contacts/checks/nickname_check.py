"""NicknameCheck class."""

from __future__ import annotations

from contacts.contact import Contact
from contacts.problem import Check, Problem


class NicknameCheck(Check):
    """Checker for nicknames."""

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""
        if contact.nickname is None:
            return []
        if len(contact.nickname.split()) > 1:
            return []
        return [Problem(f"Nickname '{contact.nickname}' is not a full name.")]

"""Problem checks."""


from __future__ import annotations

from enum import Enum

from contacts.checks import name_capitalization_check, nickname_check


class Checks(Enum):
    """List of all checkers."""

    NAME_CAPITALIZATION_CHECK = name_capitalization_check.NameCapitalizationCheck()
    NICK_NAME_CHECK = nickname_check.NicknameCheck()

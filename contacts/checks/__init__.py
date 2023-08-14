"""Problem checks."""


from __future__ import annotations

from enum import Enum

from contacts.checks.home_page_check import HomePageCheck
from contacts.checks.name_capitalization_check import NameCapitalizationCheck
from contacts.checks.nickname_check import NicknameCheck


class Checks(Enum):
    """List of all checkers."""

    NAME_CAPITALIZATION_CHECK = NameCapitalizationCheck()
    NICK_NAME_CHECK = NicknameCheck()
    HOME_PAGE_CHECK = HomePageCheck()

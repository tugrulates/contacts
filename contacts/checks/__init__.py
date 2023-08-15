"""Problem checks."""


from __future__ import annotations

from enum import Enum

from contacts.checks.capitalization_check import CapitalizationCheck
from contacts.checks.duplicate_check import DuplicateCheck
from contacts.checks.home_page_check import HomePageCheck
from contacts.checks.nickname_check import NicknameCheck
from contacts.checks.phone_check import PhoneCheck
from contacts.checks.url_check import UrlCheck


class Checks(Enum):
    """List of all checkers."""

    NAME_CAPITALIZATION_CHECK = CapitalizationCheck()
    NICK_NAME_CHECK = NicknameCheck()
    PHONE_CHECK = PhoneCheck()
    HOME_PAGE_CHECK = HomePageCheck()
    URL_CHECK = UrlCheck()
    DUPLICATE_CHECK = DuplicateCheck()  # must be the last item

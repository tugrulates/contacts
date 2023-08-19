"""Problem checks."""


from __future__ import annotations

from enum import Enum

from contacts.checks.casing_check import CasingCheck
from contacts.checks.custom_date_check import CustomDateCheck
from contacts.checks.dupe_check import DupeCheck
from contacts.checks.email_check import EmailCheck
from contacts.checks.home_page_check import HomePageCheck
from contacts.checks.label_check import LabelCheck
from contacts.checks.nickname_check import NicknameCheck
from contacts.checks.phone_check import PhoneCheck
from contacts.checks.url_check import UrlCheck
from contacts.field import ContactFields


class Checks(Enum):
    """List of all checkers."""

    PREFIX_CASING_CHECK = CasingCheck(ContactFields.PREFIX.value)
    FIRST_NAME_CASING_CHECK = CasingCheck(ContactFields.FIRST_NAME.value)
    MIDDLE_NAME_CASING_CHECK = CasingCheck(ContactFields.MIDDLE_NAME.value)
    LAST_NAME_CASING_CHECK = CasingCheck(ContactFields.LAST_NAME.value)
    MAIDEN_NAME_CASING_CHECK = CasingCheck(ContactFields.MAIDEN_NAME.value)
    SUFFIX_CASING_CHECK = CasingCheck(ContactFields.SUFFIX.value)
    NICK_NAME_CHECK = NicknameCheck()
    JOB_TITLE_CASING_CHECK = CasingCheck(ContactFields.JOB_TITLE.value)
    DEPARTMENT_CASING_CHECK = CasingCheck(ContactFields.DEPARTMENT.value)
    PHONE_LABEL_CHECK = LabelCheck(ContactFields.PHONE.value)
    PHONE_CHECK = PhoneCheck()
    PHONE_DUPE_CHECK = DupeCheck(ContactFields.PHONE.value, False)
    EMAIL_LABEL_CHECK = LabelCheck(ContactFields.EMAIL.value)
    EMAIL_CHECK = EmailCheck()
    EMAIL_DUPE_CHECK = DupeCheck(ContactFields.EMAIL.value, False)
    HOME_PAGE_CHECK = HomePageCheck()
    URL_LABEL_CHECK = LabelCheck(ContactFields.URL.value)
    URL_DUPE_CHECK = DupeCheck(ContactFields.URL.value, False)
    URL_CHECK = UrlCheck()
    ADDRESS_LABEL_CHECK = LabelCheck(ContactFields.ADDRESS.value)
    ADDRESS_DUPE_CHECK = DupeCheck(ContactFields.ADDRESS.value, False)
    CUSTOM_DATE_CHECK = CustomDateCheck()
    CUSTOM_DATE_DUPE_CHECK = DupeCheck(ContactFields.CUSTOM_DATE.value, True)
    SOCIAL_PROFILE_DUPE_CHECK = DupeCheck(ContactFields.SOCIAL_PROFILE.value, True)
    INSTANT_MESSAGE_DUPE_CHECK = DupeCheck(ContactFields.INSTANT_MESSAGE.value, True)

"""Label operations."""


from __future__ import annotations
from enum import Enum
from typing import AbstractSet, Optional


class Category(Enum):
    """A contact information category."""

    PERSON = "👤"
    COMPANY = "🏢"
    NAME = "🔖"
    PHONETIC = "🎧"
    DATE = "📅"
    PHONE = "📞"
    EMAIL = "📧"
    URL = "🌐"
    MESSAGING = "💬"
    ADDRESS = "📫"
    MOBILE = ("📱", {"_$!<Mobile>!$_"})
    HOME = ("🏠", {"_$!<Home>!$_", "_$!<Main>!$_", "_$!<HomePage>!$_"})
    WORK = ("💼", {"_$!<Work>!$_"})
    SCHOOL = ("🏫", {"_$!<School>!$_"})
    FAX = ("📠", {"_$!<HomeFAX>!$_", "_$!<WorkFAX>!$_", "_$!<OtherFAX>!$_"})
    PAGER = ("📟", {"_$!<Pager>!$_"})
    ANNIVERSARY = ("💍", {"_$!<Anniversary>!$_"})
    RELATED = "👥"
    NOTE = "📋"
    OTHER = ("❓", {"_$!<Other>!$_"})
    UNKNOWN = "❌"

    def __init__(self, icon: str, labels: AbstractSet[str] = frozenset()):
        """Initialize category."""
        self.icon = icon
        self.labels = labels

    @staticmethod
    def from_label(label: str, default: Optional[Category] = None) -> Category:
        """Return the category of given label."""
        for category in Category:
            if label in category.labels:
                return category
        return default or Category.UNKNOWN

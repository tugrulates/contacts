"""Category class."""


from __future__ import annotations

from dataclasses import Field
from enum import Enum
from typing import AbstractSet, Any, Optional


class Category(Enum):
    """A contact information category."""

    PERSON = "👤"
    COMPANY = "🏢"
    NAME = "🔖"
    PHONETIC = "🔉"
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
    OTHER = ("🗂️", {"_$!<Other>!$_"})
    WARNING = "⚠️ "
    ERROR = "⛔"

    def __init__(self, icon: str, labels: AbstractSet[str] = frozenset()):
        """Initialize category."""
        self.icon = icon
        self.labels = labels

    @staticmethod
    def from_field(field: Field[Any]) -> Optional[Category]:
        """Return the category of given Contact field."""
        return field.metadata.get("category")

    @staticmethod
    def from_label(
        label: str, default: Optional[Category] = None
    ) -> Optional[Category]:
        """Return the category of given label."""
        for category in Category:
            if label in category.labels:
                return category
        return default

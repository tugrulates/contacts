"""Contact operations."""


from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import field
from functools import cached_property
from pathlib import Path
from typing import Optional

from pydantic.dataclasses import dataclass

from contacts.category import Category
from contacts.problem import Problem, find_problems


@dataclass
class ContactInfo:
    """Single contact info."""

    info_id: str
    label: str
    value: str

    def __str__(self) -> str:
        """Short string for info."""
        return self.value


@dataclass
class ContactAddress(ContactInfo):
    """A single address."""

    country_code: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


@dataclass
class ContactSocialProfile(ContactInfo):
    """A single social profile."""

    user_identifier: Optional[str] = None
    url: Optional[str] = None

    def __str__(self) -> str:
        """Short string for profile."""
        return f"{self.value} ({self.label})"


@dataclass
class ContactInstantMessage(ContactInfo):
    """A single instant messaging profile."""

    def __str__(self) -> str:
        """Short string for profile."""
        return f"{self.value} ({self.label})"


@dataclass
class Contact:
    """A single contact person or company."""

    contact_id: str
    name: str
    is_company: bool = False
    has_image: bool = False
    prefix: Optional[str] = field(default=None, metadata={"category": Category.NAME})
    first_name: Optional[str] = field(
        default=None, metadata={"category": Category.NAME}
    )
    phonetic_first_name: Optional[str] = field(
        default=None, metadata={"category": Category.NAME}
    )
    middle_name: Optional[str] = field(
        default=None, metadata={"category": Category.NAME}
    )
    phonetic_middle_name: Optional[str] = field(
        default=None, metadata={"category": Category.NAME}
    )
    last_name: Optional[str] = field(default=None, metadata={"category": Category.NAME})
    phonetic_last_name: Optional[str] = field(
        default=None, metadata={"category": Category.NAME}
    )
    maiden_name: Optional[str] = field(
        default=None, metadata={"category": Category.NAME}
    )
    suffix: Optional[str] = field(default=None, metadata={"category": Category.NAME})
    nickname: Optional[str] = field(default=None, metadata={"category": Category.NAME})
    job_title: Optional[str] = field(default=None, metadata={"category": Category.WORK})
    department: Optional[str] = field(
        default=None, metadata={"category": Category.WORK}
    )
    organization: Optional[str] = field(
        default=None, metadata={"category": Category.WORK}
    )
    phones: list[ContactInfo] = field(
        default_factory=list, metadata={"category": Category.PHONE}
    )
    emails: list[ContactInfo] = field(
        default_factory=list, metadata={"category": Category.EMAIL}
    )
    home_page: Optional[str] = field(default=None, metadata={"category": Category.URL})
    urls: list[ContactInfo] = field(
        default_factory=list, metadata={"category": Category.URL}
    )
    addresses: list[ContactAddress] = field(
        default_factory=list, metadata={"category": Category.ADDRESS}
    )
    birth_date: Optional[str] = field(
        default=None, metadata={"category": Category.DATE}
    )
    custom_dates: list[ContactInfo] = field(
        default_factory=list, metadata={"category": Category.DATE}
    )
    related_names: list[ContactInfo] = field(
        default_factory=list, metadata={"category": Category.RELATED}
    )
    social_profiles: list[ContactSocialProfile] = field(
        default_factory=list, metadata={"category": Category.URL}
    )
    instant_messages: list[ContactInstantMessage] = field(
        default_factory=list, metadata={"category": Category.MESSAGING}
    )
    note: Optional[str] = field(default=None, metadata={"category": Category.NOTE})

    def __post_init__(self) -> None:
        """Keep a copy of the originating data to keep track of changes."""
        self._source = deepcopy(self)

    @property
    def category(self) -> Category:
        """Return the category of this info."""
        if [x for x in self.problems if x.category == Category.ERROR]:
            return Category.ERROR
        if [x for x in self.problems if x.category == Category.WARNING]:
            return Category.WARNING
        if self.is_company:
            return Category.COMPANY
        return Category.PERSON

    @cached_property
    def problems(self) -> list[Problem]:
        """Return all problems for this contact."""
        return find_problems(self)

    @staticmethod
    def read(path: Path) -> Contact:
        """Load contact from json file."""
        with path.open(encoding="utf-8") as file:
            return Contact(**json.load(file))

    def __str__(self) -> str:
        """Short string for contact."""
        return self.name

"""Contact operations."""


from __future__ import annotations

import json
from copy import deepcopy
from functools import cached_property
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from contacts.category import Category
from contacts.problem import Problem


class ContactInfo(BaseModel):
    """Single contact info."""

    id: str  # noqa: A003
    label: str
    value: str

    def __str__(self) -> str:
        """Short string for info."""
        if Category.from_label(self.label) is None:
            label = self.label.removeprefix("_$!<").removesuffix(">!$_")
            return f"{self.value} <{label}>"
        return self.value


class ContactAddress(ContactInfo):
    """A single address."""

    country_code: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class ContactSocialProfile(ContactInfo):
    """A single social profile."""

    user_identifier: Optional[str] = None
    url: Optional[str] = None


class Contact(BaseModel):
    """A single contact person or company."""

    id: str  # noqa: A003
    name: str
    is_company: bool = False
    has_image: bool = False
    prefix: Optional[str] = None
    first_name: Optional[str] = None
    phonetic_first_name: Optional[str] = None
    middle_name: Optional[str] = None
    phonetic_middle_name: Optional[str] = None
    last_name: Optional[str] = None
    phonetic_last_name: Optional[str] = None
    maiden_name: Optional[str] = None
    suffix: Optional[str] = None
    nickname: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    organization: Optional[str] = None
    phones: list[ContactInfo] = []
    emails: list[ContactInfo] = []
    home_page: Optional[str] = None
    urls: list[ContactInfo] = []
    addresses: list[ContactAddress] = []
    birth_date: Optional[str] = None
    custom_dates: list[ContactInfo] = []
    related_names: list[ContactInfo] = []
    social_profiles: list[ContactSocialProfile] = []
    instant_messages: list[ContactInfo] = []
    note: Optional[str] = None

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
        from contacts.checks import Checks

        problems = []
        for check in Checks:
            problems.extend(check.value.check(self))
        return problems

    @staticmethod
    def load(path: Path) -> Contact:
        """Load contact from json file."""
        with path.open(encoding="utf-8") as file:
            return Contact(**json.load(file))

    def __str__(self) -> str:
        """Short string for contact."""
        return self.name


class Contacts(BaseModel):
    """A list of contacts."""

    contacts: list[Contact] = []

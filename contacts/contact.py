"""Contact operations."""


from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import field
from functools import cached_property
from pathlib import Path
from typing import Optional

from pydantic import RootModel
from pydantic.dataclasses import dataclass

from contacts.category import Category
from contacts.problem import Problem


@dataclass
class ContactInfo:
    """Single contact info."""

    info_id: str
    label: str
    value: str

    def __str__(self) -> str:
        """Short string for info."""
        if Category.from_label(self.label) is None:
            label = self.label.removeprefix("_$!<").removesuffix(">!$_")
            return f"{self.value} <{label}>"
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


@dataclass
class Contact:
    """A single contact person or company."""

    contact_id: str
    name: str
    is_company: bool = False
    has_image: bool = False
    prefix: Optional[str] = field(default=None)
    first_name: Optional[str] = field(default=None)
    phonetic_first_name: Optional[str] = field(default=None)
    middle_name: Optional[str] = field(default=None)
    phonetic_middle_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)
    phonetic_last_name: Optional[str] = field(default=None)
    maiden_name: Optional[str] = field(default=None)
    suffix: Optional[str] = field(default=None)
    nickname: Optional[str] = field(default=None)
    job_title: Optional[str] = field(default=None)
    department: Optional[str] = field(default=None)
    organization: Optional[str] = field(default=None)
    phones: list[ContactInfo] = field(default_factory=list)
    emails: list[ContactInfo] = field(default_factory=list)
    home_page: Optional[str] = field(default=None)
    urls: list[ContactInfo] = field(default_factory=list)
    addresses: list[ContactAddress] = field(default_factory=list)
    birth_date: Optional[str] = field(default=None)
    custom_dates: list[ContactInfo] = field(default_factory=list)
    related_names: list[ContactInfo] = field(default_factory=list)
    social_profiles: list[ContactSocialProfile] = field(default_factory=list)
    instant_messages: list[ContactInfo] = field(default_factory=list)
    note: Optional[str] = field(default=None)

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


@dataclass
class Contacts:
    """A list of contacts."""

    contacts: list[Contact] = field(default_factory=list)

    def dumps(self) -> str:
        """Dump JSON string."""
        return RootModel[Contacts](self).model_dump_json(exclude_defaults=True)

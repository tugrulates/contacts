"""Contact operations."""


from __future__ import annotations

import dataclasses
import json
from copy import deepcopy
from dataclasses import field
from functools import cached_property
from pathlib import Path
from typing import Optional

from pydantic import RootModel
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
class FieldMetadata:
    """Metadata on Contact fields."""

    category: Category
    singular: str
    plural_suffix: str = "s"

    def plural(self) -> str:
        """Return plural display value."""
        return self.singular + self.plural_suffix


@dataclass
class Contact:
    """A single contact person or company."""

    contact_id: str
    name: str
    is_company: bool = False
    has_image: bool = False
    prefix: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Prefix")},
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "First name")},
    )
    phonetic_first_name: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Phonetic first name")},
    )
    middle_name: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Middle name")},
    )
    phonetic_middle_name: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Phonetic middle name")},
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Last name")},
    )
    phonetic_last_name: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Phonetic last name")},
    )
    maiden_name: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Maiden name")},
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Suffix")},
    )
    nickname: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NAME, "Nickname")},
    )
    job_title: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.WORK, "Job title")},
    )
    department: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.WORK, "Department")},
    )
    organization: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.WORK, "Organization")},
    )
    phones: list[ContactInfo] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.PHONE, "Phone")},
    )
    emails: list[ContactInfo] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.EMAIL, "E-mail")},
    )
    home_page: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.URL, "Home page")},
    )
    urls: list[ContactInfo] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.URL, "URL")},
    )
    addresses: list[ContactAddress] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.ADDRESS, "Address", "es")},
    )
    birth_date: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.DATE, "Birth date")},
    )
    custom_dates: list[ContactInfo] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.DATE, "Custom date")},
    )
    related_names: list[ContactInfo] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.RELATED, "Related name")},
    )
    social_profiles: list[ContactSocialProfile] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.URL, "Social profile")},
    )
    instant_messages: list[ContactInfo] = field(
        default_factory=list,
        metadata={"metadata": FieldMetadata(Category.MESSAGING, "Instant message")},
    )
    note: Optional[str] = field(
        default=None,
        metadata={"metadata": FieldMetadata(Category.NOTE, "Note")},
    )

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
    def metadata(field: str) -> Optional[FieldMetadata]:
        """Return metadata for a contact field."""
        metadata: list[FieldMetadata] = [
            x.metadata["metadata"]
            for x in dataclasses.fields(Contact)
            if x.name == field and "metadata" in x.metadata
        ]
        return metadata[0] if metadata else None

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

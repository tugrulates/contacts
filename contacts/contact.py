"""Contact operations."""


import json
from itertools import zip_longest
from typing import Any, Iterator, Optional

from contacts import applescript
from contacts.category import Category


class Info:
    """A single info with an icon."""

    def __init__(self, category: Category, value: str):
        """Initialize info from query output."""
        self._category = category
        self._value = value

    @property
    def category(self) -> Category:
        """Return the category of this info."""
        return self._category

    @property
    def icon(self) -> str:
        """Return the icon of this info."""
        return self.category.icon

    @property
    def value(self) -> str:
        """Return the value of this info."""
        return self._value

    def __str__(self) -> str:
        """Convert info to string."""
        value_str = self.value.replace("\n", "\n   ")
        return f"{self.icon} {value_str}"

    def __repr__(self) -> str:
        """Info object repr."""
        return f"{type(self)}({self.value})"


class RichInfo(Info):
    """An multi-value info with an id."""

    def __init__(self, category: Category, data: dict[str, Any]):
        """Initialize info from query output."""
        self._category = category
        self._data = data

    @property
    def info_id(self) -> str:
        """Return the id of this info."""
        return str(self._data["id"])

    @property
    def icon(self) -> str:
        """Return the icon of this info."""
        return Category.from_label(self.label, self.category).icon

    @property
    def label(self) -> str:
        """Return the label of this info."""
        return str(self._data["label"])

    @property
    def value(self) -> str:
        """Return the value of this info."""
        return str(self._data["value"])


class Address(RichInfo):
    """A single address."""

    @property
    def value(self) -> str:
        """Return the value of this info."""
        return self.formatted_address or ""

    @property
    def country_code(self) -> Optional[str]:
        """Return the country code of this address."""
        data = self._data["country_code"]
        return str(data) if data else None

    @property
    def street(self) -> Optional[str]:
        """Return the street info of this address."""
        data = self._data["street"]
        return str(data) if data else None

    @property
    def city(self) -> Optional[str]:
        """Return the city of this address."""
        data = self._data["city"]
        return str(data) if data else None

    @property
    def state(self) -> Optional[str]:
        """Return the state of this address."""
        data = self._data["state"]
        return str(data) if data else None

    @property
    def zip_code(self) -> Optional[str]:
        """Return the zip code of this address."""
        data = self._data["zip"]
        return str(data) if data else None

    @property
    def country(self) -> Optional[str]:
        """Return the country of this address."""
        data = self._data["country"]
        return str(data) if data else None

    @property
    def formatted_address(self) -> Optional[str]:
        """Return the formatted address of this address."""
        data = self._data["formatted_address"]
        return str(data) if data else None


class OnlineProfile(RichInfo):
    """A single social profile or instant message address."""

    @property
    def label(self) -> str:
        """Return the label of this social profile."""
        return self.service_name or "unknown"

    @property
    def value(self) -> str:
        """Return the value of this social profile."""
        return f"{self.user_name} ({self.service_name})"

    @property
    def service_name(self) -> Optional[str]:
        """Return the service name of this social profile."""
        data = self._data["service_name"]
        return str(data) if data else None

    @property
    def user_name(self) -> Optional[str]:
        """Return the user name of this social profile."""
        data = self._data["user_name"]
        return str(data) if data else None


class SocialProfile(OnlineProfile):
    """A single social profile."""

    @property
    def user_identifier(self) -> Optional[str]:
        """Return the user identifier of this social profile."""
        data = self._data["user_identifier"]
        return str(data) if data else None

    @property
    def url(self) -> Optional[str]:
        """Return the url of this social profile."""
        data = self._data["url"]
        return str(data) if data else None


class Contact(RichInfo):
    """A single contact person or company."""

    def __init__(self, data: dict[str, Any]):
        """Initialize info from query output."""
        self._data = data

    @property
    def value(self) -> str:
        """Use contact name as info value."""
        return self.name

    @property
    def category(self) -> Category:
        """Return the category of this info."""
        return Category.COMPANY if self.is_company else Category.PERSON

    @property
    def contact_id(self) -> str:
        """Return the id of this contact."""
        return str(self._data["id"])

    @property
    def icon(self) -> str:
        """Return the icon of this contact."""
        return self.category.icon

    @property
    def name(self) -> str:
        """Return the full name of this contact."""
        return str(self._data["name"])

    @property
    def has_image(self) -> bool:
        """Return whether this contact has an image."""
        return bool(self._data["has_image"])

    @property
    def is_company(self) -> bool:
        """Return whether this contact is a company."""
        return bool(self._data["company"])

    @property
    def prefix(self) -> Optional[Info]:
        """Return the prefix of this contact."""
        data = self._data.get("prefix")
        return Info(Category.NAME, data) if data else None

    @property
    def first_name(self) -> Optional[Info]:
        """Return the first name of this contact."""
        data = self._data.get("first_name")
        return Info(Category.NAME, data) if data else None

    @property
    def phonetic_first_name(self) -> Optional[Info]:
        """Return the phonetic version of the first name of this contact."""
        data = self._data.get("phonetic_first_name")
        return Info(Category.PHONETIC, data) if data else None

    @property
    def middle_name(self) -> Optional[Info]:
        """Return the middle name of this contact."""
        data = self._data.get("middle_name")
        return Info(Category.NAME, data) if data else None

    @property
    def phonetic_middle_name(self) -> Optional[Info]:
        """Return the phonetic version of the middle name of this contact."""
        data = self._data.get("phonetic_middle_name")
        return Info(Category.PHONETIC, data) if data else None

    @property
    def last_name(self) -> Optional[Info]:
        """Return the last name of this contact."""
        data = self._data.get("last_name")
        return Info(Category.NAME, data) if data else None

    @property
    def phonetic_last_name(self) -> Optional[Info]:
        """Return the phonetic version of the last name of this contact."""
        data = self._data.get("phonetic_last_name")
        return Info(Category.PHONETIC, data) if data else None

    @property
    def maiden_name(self) -> Optional[Info]:
        """Return the maiden name of this contact."""
        data = self._data.get("maiden_name")
        return Info(Category.NAME, data) if data else None

    @property
    def suffix(self) -> Optional[Info]:
        """Return the suffix of this contact."""
        data = self._data.get("suffix")
        return Info(Category.NAME, data) if data else None

    @property
    def nickname(self) -> Optional[Info]:
        """Return the nickname of this contact."""
        data = self._data.get("nickname")
        return Info(Category.NAME, data) if data else None

    @property
    def job_title(self) -> Optional[Info]:
        """Return the job title of this contact."""
        data = self._data.get("job_title")
        return Info(Category.WORK, data) if data else None

    @property
    def department(self) -> Optional[Info]:
        """Return the department this contact works for."""
        data = self._data.get("department")
        return Info(Category.WORK, data) if data else None

    @property
    def organization(self) -> Optional[Info]:
        """Return the organization this contact works for."""
        data = self._data.get("organization")
        return Info(Category.WORK, data) if data else None

    @property
    def phones(self) -> list[RichInfo]:
        """Return the phones of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("phones")
        return [RichInfo(Category.PHONE, x) for x in data] if data else []

    @property
    def emails(self) -> list[RichInfo]:
        """Return the emails of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("emails")
        return [RichInfo(Category.EMAIL, x) for x in data] if data else []

    @property
    def home_page(self) -> Optional[Info]:
        """Return the home page of this contact."""
        data = self._data.get("home_page")
        return Info(Category.URL, data) if data else None

    @property
    def urls(self) -> list[RichInfo]:
        """Return the URLs of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("urls")
        return [RichInfo(Category.URL, x) for x in data] if data else []

    @property
    def addresses(self) -> list[Address]:
        """Return the addresses of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("addresses")
        return [Address(Category.ADDRESS, x) for x in data] if data else []

    @property
    def birth_date(self) -> Optional[Info]:
        """Return the birth date of this contact."""
        data = self._data.get("birth_date")
        return Info(Category.DATE, data) if data else None

    @property
    def custom_dates(self) -> list[RichInfo]:
        """Return the custom dates of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("custom_dates")
        return [RichInfo(Category.DATE, x) for x in data] if data else []

    @property
    def related_names(self) -> list[RichInfo]:
        """Return the related names of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("related_names")
        return [RichInfo(Category.RELATED, x) for x in data] if data else []

    @property
    def social_profiles(self) -> list[SocialProfile]:
        """Return the social profiles of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("social_profiles")
        return [SocialProfile(Category.URL, x) for x in data] if data else []

    @property
    def instant_messages(self) -> list[OnlineProfile]:
        """Return the instant message addresses of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("instant_messages")
        return [OnlineProfile(Category.MESSAGING, x) for x in data] if data else []

    @property
    def note(self) -> Optional[Info]:
        """Return the notes for this contact."""
        data = self._data.get("note")
        return Info(Category.NOTE, data) if data else None

    def details(self) -> dict[str, Any]:
        """Printable details of the contact."""
        details = {
            prop: self.__getattribute__(prop)
            for prop in [
                "prefix",
                "first_name",
                "phonetic_first_name",
                "middle_name",
                "phonetic_middle_name",
                "last_name",
                "phonetic_last_name",
                "maiden_name",
                "suffix",
                "nickname",
                "job_title",
                "department",
                "organization",
                "phones",
                "emails",
                "home_page",
                "urls",
                "addresses",
                "birth_date",
                "custom_dates",
                "related_names",
                "social_profiles",
                "instant_messages",
                "note",
            ]
        }
        return {k: v for k, v in details.items() if v}


def count(keywords: list[str]) -> int:
    """Return the list of contacts matching keywords without loading them."""
    output = applescript.run_and_read_output("find", "?", *keywords)
    return int(output)


def by_keyword(
    keywords: list[str], *, brief: bool = False, batch: int = 1
) -> Iterator[Contact]:
    """Find contacts matching given keyword.

    :param batch: batch detail queries by given number of contacts
    """
    contact_ids = applescript.run_and_read_log("find", *keywords)
    chunks = zip_longest(*([iter(contact_ids)] * batch))
    for chunk in chunks:
        yield from by_id([x for x in chunk if x], brief=brief)


def by_id(contact_ids: list[str], *, brief: bool = False) -> Iterator[Contact]:
    """Create contact by id."""
    script = "brief" if brief else "detail"
    result = json.loads(applescript.run_and_read_output(script, *contact_ids))
    for contact in result:
        yield Contact(contact)

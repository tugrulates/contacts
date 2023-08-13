"""Contact operations."""


from functools import cached_property
from typing import Any, Optional

from contacts import problem
from contacts.category import Category
from contacts.info import ContactInfo, Info, SimpleInfo
from contacts.problem import Problem

DataType = dict[str, Any]


class ContactPhone(ContactInfo):
    """Phone of a contact."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        ContactInfo.__init__(self, Category.PHONE, data)


class ContactEmail(ContactInfo):
    """Email of a contact."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        ContactInfo.__init__(self, Category.EMAIL, data)


class ContactUrl(ContactInfo):
    """Url of a contact."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        ContactInfo.__init__(self, Category.URL, data)


class ContactDate(SimpleInfo):
    """Date of a contact."""

    def __init__(self, value: str):
        """Initialize info from query output."""
        SimpleInfo.__init__(self, Category.DATE, value)


class ContactCustomDate(ContactInfo):
    """Date of a contact."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        ContactInfo.__init__(self, Category.DATE, data)


class ContactRelatedName(ContactInfo):
    """Related name of a contact."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        ContactInfo.__init__(self, Category.RELATED, data)


class ContactAddress(ContactInfo):
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


class ContactOnlineProfile(ContactInfo):
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


class ContactSocialProfile(ContactOnlineProfile):
    """A single social profile."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        ContactInfo.__init__(self, Category.URL, data)

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


class ContactInstantMessage(ContactOnlineProfile):
    """A single instant message profile."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        ContactInfo.__init__(self, Category.MESSAGING, data)


class Contact(Info):
    """A single contact person or company."""

    def __init__(self, data: DataType):
        """Initialize info from query output."""
        self._data = data

    @property
    def value(self) -> str:
        """Use contact name as info value."""
        return self.name

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
    def prefix(self) -> Optional[SimpleInfo]:
        """Return the prefix of this contact."""
        data = self._data.get("prefix")
        return SimpleInfo(Category.NAME, data) if data else None

    @property
    def first_name(self) -> Optional[SimpleInfo]:
        """Return the first name of this contact."""
        data = self._data.get("first_name")
        return SimpleInfo(Category.NAME, data) if data else None

    @property
    def phonetic_first_name(self) -> Optional[SimpleInfo]:
        """Return the phonetic version of the first name of this contact."""
        data = self._data.get("phonetic_first_name")
        return SimpleInfo(Category.PHONETIC, data) if data else None

    @property
    def middle_name(self) -> Optional[SimpleInfo]:
        """Return the middle name of this contact."""
        data = self._data.get("middle_name")
        return SimpleInfo(Category.NAME, data) if data else None

    @property
    def phonetic_middle_name(self) -> Optional[SimpleInfo]:
        """Return the phonetic version of the middle name of this contact."""
        data = self._data.get("phonetic_middle_name")
        return SimpleInfo(Category.PHONETIC, data) if data else None

    @property
    def last_name(self) -> Optional[SimpleInfo]:
        """Return the last name of this contact."""
        data = self._data.get("last_name")
        return SimpleInfo(Category.NAME, data) if data else None

    @property
    def phonetic_last_name(self) -> Optional[SimpleInfo]:
        """Return the phonetic version of the last name of this contact."""
        data = self._data.get("phonetic_last_name")
        return SimpleInfo(Category.PHONETIC, data) if data else None

    @property
    def maiden_name(self) -> Optional[SimpleInfo]:
        """Return the maiden name of this contact."""
        data = self._data.get("maiden_name")
        return SimpleInfo(Category.NAME, data) if data else None

    @property
    def suffix(self) -> Optional[SimpleInfo]:
        """Return the suffix of this contact."""
        data = self._data.get("suffix")
        return SimpleInfo(Category.NAME, data) if data else None

    @property
    def nickname(self) -> Optional[SimpleInfo]:
        """Return the nickname of this contact."""
        data = self._data.get("nickname")
        return SimpleInfo(Category.NAME, data) if data else None

    @property
    def job_title(self) -> Optional[SimpleInfo]:
        """Return the job title of this contact."""
        data = self._data.get("job_title")
        return SimpleInfo(Category.WORK, data) if data else None

    @property
    def department(self) -> Optional[SimpleInfo]:
        """Return the department this contact works for."""
        data = self._data.get("department")
        return SimpleInfo(Category.WORK, data) if data else None

    @property
    def organization(self) -> Optional[SimpleInfo]:
        """Return the organization this contact works for."""
        data = self._data.get("organization")
        return SimpleInfo(Category.WORK, data) if data else None

    @property
    def phones(self) -> list[ContactPhone]:
        """Return the phones of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("phones")
        return [ContactPhone(x) for x in data or []]

    @property
    def emails(self) -> list[ContactEmail]:
        """Return the emails of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("emails")
        return [ContactEmail(x) for x in data or []]

    @property
    def home_page(self) -> Optional[SimpleInfo]:
        """Return the home page of this contact."""
        data = self._data.get("home_page")
        return SimpleInfo(Category.URL, data) if data else None

    @property
    def urls(self) -> list[ContactUrl]:
        """Return the URLs of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("urls")
        return [ContactUrl(x) for x in data] if data else []

    @property
    def addresses(self) -> list[ContactAddress]:
        """Return the addresses of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("addresses")
        return [ContactAddress(Category.ADDRESS, x) for x in data] if data else []

    @property
    def birth_date(self) -> Optional[ContactDate]:
        """Return the birth date of this contact."""
        data = self._data.get("birth_date")
        return ContactDate(data) if data else None

    @property
    def custom_dates(self) -> list[ContactCustomDate]:
        """Return the custom dates of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("custom_dates")
        return [ContactCustomDate(x) for x in data or []]

    @property
    def related_names(self) -> list[ContactRelatedName]:
        """Return the related names of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("related_names")
        return [ContactRelatedName(x) for x in data or []]

    @property
    def social_profiles(self) -> list[ContactSocialProfile]:
        """Return the social profiles of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("social_profiles")
        return [ContactSocialProfile(x) for x in data or []]

    @property
    def instant_messages(self) -> list[ContactInstantMessage]:
        """Return the instant message addresses of this contact."""
        data: Optional[list[dict[str, Any]]] = self._data.get("instant_messages")
        return [ContactInstantMessage(x) for x in data or []]

    @property
    def note(self) -> Optional[SimpleInfo]:
        """Return the notes for this contact."""
        data = self._data.get("note")
        return SimpleInfo(Category.NOTE, data) if data else None

    @cached_property
    def problems(self) -> list[Problem]:
        """Return all problems for this contact."""
        return problem.find_problems(self)

"""Contact field metadata."""

from enum import Enum
from typing import Callable, NamedTuple, Optional, Sequence

from contacts.address_book import AddressBook
from contacts.category import Category
from contacts.contact import Contact, ContactInfo


class ContactFieldMetadata(NamedTuple):
    """Types for simple field metadata."""

    singular: str
    category: Category
    get: Callable[[Contact], Optional[str]]
    update: AddressBook.UpdateFieldFunction
    delete: AddressBook.DeleteFieldFunction


class ContactInfoMetadata(NamedTuple):
    """Types for simple field metadata."""

    singular: str
    plural: str
    category: Category
    get: Callable[[Contact], Sequence[ContactInfo]]
    update: AddressBook.UpdateInfoLabelFunction
    delete: AddressBook.DeleteInfoFunction


class ContactFields(Enum):
    """Field metadatas."""

    PREFIX = ContactFieldMetadata(
        "Prefix",
        Category.NAME,
        lambda contact: contact.prefix,
        AddressBook.update_prefix,
        AddressBook.delete_prefix,
    )
    FIRST_NAME = ContactFieldMetadata(
        "First name",
        Category.NAME,
        lambda contact: contact.first_name,
        AddressBook.update_first_name,
        AddressBook.delete_first_name,
    )
    PHONETIC_FIRST_NAME = ContactFieldMetadata(
        "Phonetic first name",
        Category.NAME,
        lambda contact: contact.phonetic_first_name,
        AddressBook.update_phonetic_first_name,
        AddressBook.delete_phonetic_first_name,
    )
    MIDDLE_NAME = ContactFieldMetadata(
        "Middle name",
        Category.NAME,
        lambda contact: contact.middle_name,
        AddressBook.update_middle_name,
        AddressBook.delete_middle_name,
    )
    PHONETIC_MIDDLE_NAME = ContactFieldMetadata(
        "Phonetic middle name",
        Category.NAME,
        lambda contact: contact.phonetic_middle_name,
        AddressBook.update_phonetic_middle_name,
        AddressBook.delete_phonetic_middle_name,
    )
    LAST_NAME = ContactFieldMetadata(
        "Last name",
        Category.NAME,
        lambda contact: contact.last_name,
        AddressBook.update_last_name,
        AddressBook.delete_last_name,
    )
    PHONETIC_LAST_NAME = ContactFieldMetadata(
        "Phonetic last name",
        Category.NAME,
        lambda contact: contact.phonetic_last_name,
        AddressBook.update_phonetic_last_name,
        AddressBook.delete_phonetic_last_name,
    )
    MAIDEN_NAME = ContactFieldMetadata(
        "Maiden name",
        Category.NAME,
        lambda contact: contact.maiden_name,
        AddressBook.update_maiden_name,
        AddressBook.delete_maiden_name,
    )
    SUFFIX = ContactFieldMetadata(
        "Suffix",
        Category.NAME,
        lambda contact: contact.suffix,
        AddressBook.update_suffix,
        AddressBook.delete_suffix,
    )
    NICKNAME = ContactFieldMetadata(
        "Nickname",
        Category.NAME,
        lambda contact: contact.nickname,
        AddressBook.update_nickname,
        AddressBook.delete_nickname,
    )
    JOB_TITLE = ContactFieldMetadata(
        "Job title",
        Category.WORK,
        lambda contact: contact.job_title,
        AddressBook.update_job_title,
        AddressBook.delete_job_title,
    )
    DEPARTMENT = ContactFieldMetadata(
        "Department",
        Category.WORK,
        lambda contact: contact.department,
        AddressBook.update_department,
        AddressBook.delete_department,
    )
    ORGANIZATION = ContactFieldMetadata(
        "Organization",
        Category.WORK,
        lambda contact: contact.organization,
        AddressBook.update_organization,
        AddressBook.delete_organization,
    )
    PHONE = ContactInfoMetadata(
        "Phone",
        "Phones",
        Category.PHONE,
        lambda contact: contact.phones,
        AddressBook.update_phone,
        AddressBook.delete_phone,
    )
    EMAIL = ContactInfoMetadata(
        "E-mail",
        "E-mails",
        Category.EMAIL,
        lambda contact: contact.emails,
        AddressBook.update_email,
        AddressBook.delete_email,
    )
    HOME_PAGE = ContactFieldMetadata(
        "Home page",
        Category.URL,
        lambda contact: contact.home_page,
        AddressBook.update_home_page,
        AddressBook.delete_home_page,
    )
    URL = ContactInfoMetadata(
        "URL",
        "URLs",
        Category.URL,
        lambda contact: contact.urls,
        AddressBook.update_url,
        AddressBook.delete_url,
    )
    ADDRESS = ContactInfoMetadata(
        "Address",
        "Addresses",
        Category.ADDRESS,
        lambda contact: contact.addresses,
        AddressBook.update_address,
        AddressBook.delete_address,
    )
    BIRTH_DATE = ContactFieldMetadata(
        "Birth date",
        Category.DATE,
        lambda contact: contact.birth_date,
        AddressBook.update_birth_date,
        AddressBook.delete_birth_date,
    )
    CUSTOM_DATE = ContactInfoMetadata(
        "Custom date",
        "Custom dates",
        Category.DATE,
        lambda contact: contact.custom_dates,
        AddressBook.update_custom_date,
        AddressBook.delete_custom_date,
    )
    RELATED_NAME = ContactInfoMetadata(
        "Related name",
        "Related names",
        Category.RELATED,
        lambda contact: contact.related_names,
        AddressBook.update_related_name,
        AddressBook.delete_related_name,
    )
    SOCIAL_PROFILE = ContactInfoMetadata(
        "Social profile",
        "Social profiles",
        Category.URL,
        lambda contact: contact.social_profiles,
        AddressBook.update_social_profile,
        AddressBook.delete_social_profile,
    )
    INSTANT_MESSAGE = ContactInfoMetadata(
        "Instant message",
        "Instant messages",
        Category.MESSAGING,
        lambda contact: contact.instant_messages,
        AddressBook.update_instant_message,
        AddressBook.delete_instant_message,
    )
    NOTE = ContactFieldMetadata(
        "Note",
        Category.NOTE,
        lambda contact: contact.note,
        AddressBook.update_note,
        AddressBook.delete_note,
    )

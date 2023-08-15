"""Address book queries through applescript code."""

import json
import subprocess  # nosec B404
from itertools import zip_longest
from pathlib import Path
from typing import Iterator

from contacts.contact import Contact, ContactInfo


def _run_and_read_output(script: str, *args: str) -> str:
    """Run a named script with arguments and return the stdout."""
    script_path = (
        Path(__file__).parent / "applescript" / "{}.applescript".format(script)
    )
    result = None
    try:
        result = subprocess.run(
            ["/usr/bin/osascript", script_path, *args],
            encoding="utf-8",
            check=True,
            capture_output=True,
        )  # nosec B603
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise e


def _run_and_read_log(script: str, *args: str) -> Iterator[str]:
    """Run a named script with arguments and return the stdout."""
    script_path = (
        Path(__file__).parent / "applescript" / "{}.applescript".format(script)
    )
    try:
        with subprocess.Popen(
            ["/usr/bin/osascript", script_path, *args],
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        ) as process:  # nosec B603
            if process.stderr:
                yield from (x.strip() for x in process.stderr)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise e


def count(keywords: list[str]) -> int:
    """Return number of contacts matching given keywords."""
    return int(_run_and_read_output("find", "?", *keywords))


def by_keyword(
    keywords: list[str], *, brief: bool = False, batch: int = 1
) -> Iterator[Contact]:
    """Return list of contact ids matching given keywords."""
    contact_ids = _run_and_read_log("find", *keywords)
    chunks = zip_longest(*([iter(contact_ids)] * batch))
    for chunk in list(chunks):
        yield from by_id([x for x in chunk if x], brief=brief)


def by_id(contact_ids: list[str], *, brief: bool = False) -> Iterator[Contact]:
    """Return contacts with given ids.

    :param brief: omit most contact details in favor of performance
    """
    output = _run_and_read_output("brief" if brief else "detail", *contact_ids)
    for data in json.loads(output):
        yield Contact(**data)


def reload(contact: Contact) -> Contact:
    """Fetch a contact again."""
    result = list(by_id([contact.contact_id]))
    if not result:
        raise RuntimeError("Contact not found {contact.contact_id}")
    return result[0]


def update_prefix(contact: Contact, value: str) -> str:
    """Update contact prefix with given value."""
    return _run_and_read_output("update", contact.contact_id, "prefix", value)


def update_first_name(contact: Contact, value: str) -> str:
    """Update contact first name with given value."""
    return _run_and_read_output("update", contact.contact_id, "first_name", value)


def update_middle_name(contact: Contact, value: str) -> str:
    """Update contact middle name with given value."""
    return _run_and_read_output("update", contact.contact_id, "middle_name", value)


def update_last_name(contact: Contact, value: str) -> str:
    """Update contact last name with given value."""
    return _run_and_read_output("update", contact.contact_id, "last_name", value)


def update_maiden_name(contact: Contact, value: str) -> str:
    """Update contact maiden name with given value."""
    return _run_and_read_output("update", contact.contact_id, "maiden_name", value)


def update_suffix(contact: Contact, value: str) -> str:
    """Update contact suffix with given value."""
    return _run_and_read_output("update", contact.contact_id, "suffix", value)


def update_nickname(contact: Contact, value: str) -> str:
    """Update contact nickname with given value."""
    return _run_and_read_output("update", contact.contact_id, "nickname", value)


def update_job_title(contact: Contact, value: str) -> str:
    """Update contact job title with given value."""
    return _run_and_read_output("update", contact.contact_id, "job_title", value)


def update_department(contact: Contact, value: str) -> str:
    """Update contact department with given value."""
    return _run_and_read_output("update", contact.contact_id, "department", value)


def update_organization(contact: Contact, value: str) -> str:
    """Update contact organization with given value."""
    return _run_and_read_output("update", contact.contact_id, "organization", value)


def update_phone(contact: Contact, phone: ContactInfo, label: str, value: str) -> str:
    """Update contact phone with given label and value."""
    return _run_and_read_output(
        "update", contact.contact_id, "phones", phone.info_id, label, value
    )


def update_url(contact: Contact, url: ContactInfo, label: str, value: str) -> str:
    """Update contact url with given label and value."""
    return _run_and_read_output(
        "update", contact.contact_id, "urls", url.info_id, label, value
    )


def add_phone(contact: Contact, label: str, value: str) -> str:
    """Add a contact phone."""
    return _run_and_read_output("add", contact.contact_id, "phones", label, value)


def add_url(contact: Contact, label: str, value: str) -> str:
    """Add a contact URL."""
    return _run_and_read_output("add", contact.contact_id, "urls", label, value)


def delete_phone(contact: Contact, phone: ContactInfo) -> str:
    """Delete contact phone."""
    return _run_and_read_output("delete", contact.contact_id, "phones", phone.info_id)


def delete_email(contact: Contact, email: ContactInfo) -> str:
    """Delete contact email."""
    return _run_and_read_output("delete", contact.contact_id, "emails", email.info_id)


def delete_home_page(contact: Contact) -> str:
    """Delete contact home page."""
    return _run_and_read_output("delete", contact.contact_id, "home_page")


def delete_url(contact: Contact, url: ContactInfo) -> str:
    """Delete contact url."""
    return _run_and_read_output("delete", contact.contact_id, "urls", url.info_id)


def delete_address(contact: Contact, address: ContactInfo) -> str:
    """Delete contact address."""
    return _run_and_read_output(
        "delete", contact.contact_id, "addresses", address.info_id
    )


def delete_custom_date(contact: Contact, custom_date: ContactInfo) -> str:
    """Delete contact custom date."""
    return _run_and_read_output(
        "delete", contact.contact_id, "custom_dates", custom_date.info_id
    )


def delete_social_profile(contact: Contact, social_profile: ContactInfo) -> str:
    """Delete contact social profile."""
    return _run_and_read_output(
        "delete", contact.contact_id, "social_profiles", social_profile.info_id
    )


def delete_instant_message(contact: Contact, instant_message: ContactInfo) -> str:
    """Delete contact instant message."""
    return _run_and_read_output(
        "delete", contact.contact_id, "instant_messages", instant_message.info_id
    )

"""Address book queries through applescript code."""

import json
import subprocess  # nosec B404
from itertools import zip_longest
from pathlib import Path
from typing import Iterator

from contacts.contact import Contact, ContactPhone


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
        yield Contact(data)


def reload(contact: Contact) -> Contact:
    """Fetch a contact again."""
    result = list(by_id([contact.contact_id]))
    if not result:
        raise RuntimeError("Contact not found {contact.contact_id}")
    return result[0]


def update_prefix(contact: Contact, value: str) -> str:
    """Update contact prefix with given value."""
    return _run_and_read_output("update", "prefix", value, contact.contact_id)


def update_first_name(contact: Contact, value: str) -> str:
    """Update contact first name with given value."""
    return _run_and_read_output("update", "first_name", value, contact.contact_id)


def update_middle_name(contact: Contact, value: str) -> str:
    """Update contact middle name with given value."""
    return _run_and_read_output("update", "middle_name", value, contact.contact_id)


def update_last_name(contact: Contact, value: str) -> str:
    """Update contact last name with given value."""
    return _run_and_read_output("update", "last_name", value, contact.contact_id)


def update_maiden_name(contact: Contact, value: str) -> str:
    """Update contact maiden name with given value."""
    return _run_and_read_output("update", "maiden_name", value, contact.contact_id)


def update_suffix(contact: Contact, value: str) -> str:
    """Update contact suffix with given value."""
    return _run_and_read_output("update", "suffix", value, contact.contact_id)


def update_nickname(contact: Contact, value: str) -> str:
    """Update contact nickname with given value."""
    return _run_and_read_output("update", "nickname", value, contact.contact_id)


def update_job_title(contact: Contact, value: str) -> str:
    """Update contact job title with given value."""
    return _run_and_read_output("update", "job_title", value, contact.contact_id)


def update_department(contact: Contact, value: str) -> str:
    """Update contact department with given value."""
    return _run_and_read_output("update", "department", value, contact.contact_id)


def update_organization(contact: Contact, value: str) -> str:
    """Update contact organization with given value."""
    return _run_and_read_output("update", "organization", value, contact.contact_id)


def update_phone(contact: Contact, phone: ContactPhone, value: str) -> str:
    """Update contact phone with given value."""
    return _run_and_read_output(
        "update", "phone", value, contact.contact_id, phone.info_id
    )

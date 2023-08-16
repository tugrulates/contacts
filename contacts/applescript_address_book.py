"""AppleScriptAddressBook class."""


from __future__ import annotations

import json
import subprocess  # nosec B404
from itertools import zip_longest
from pathlib import Path
from typing import Iterator

from contacts.address_book import AddressBook
from contacts.contact import Contact


class AppleScriptBasedAddressBook(AddressBook):
    """Address book implementation using AppleScript."""

    def __init__(self, brief: bool, batch: int):
        """Initialize with configuration."""
        self.brief = brief
        self.batch = batch

    def _run_and_read_output(self, script: str, *args: str) -> str:
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

    def _run_and_read_log(self, script: str, *args: str) -> Iterator[str]:
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

    def count(self, keywords: list[str]) -> int:
        """Return number of contacts matching given keywords."""
        return int(self._run_and_read_output("find", "?", *keywords))

    def find(self, keywords: list[str]) -> Iterator[Contact]:
        """Return list of contact ids matching given keywords."""
        contact_ids = self._run_and_read_log("find", *keywords)
        chunks = zip_longest(*([iter(contact_ids)] * self.batch))
        for chunk in list(chunks):
            yield from self._by_id([x for x in chunk if x], brief=self.brief)

    def get(self, contact_id: str) -> Contact:
        """Fetch a contact with its id."""
        result = list(self._by_id([contact_id]))
        if not result:
            raise RuntimeError("Contact not found {contact.contact_id}")
        return result[0]

    def _by_id(
        self, contact_ids: list[str], *, brief: bool = False
    ) -> Iterator[Contact]:
        """Return contacts with given ids.

        :param brief: omit most contact details in favor of performance
        """
        output = self._run_and_read_output("brief" if brief else "detail", *contact_ids)
        for data in json.loads(output):
            yield Contact(**data)

    def update_field(self, contact_id: str, field: str, value: str) -> None:
        """Update contact field with given value."""
        self._run_and_read_output("update", contact_id, field, value)

    def delete_field(self, contact_id: str, field: str) -> None:
        """Delete a contact field."""
        self._run_and_read_output("delete", contact_id, field)

    def update_info(
        self, contact_id: str, field: str, info_id: str, label: str, value: str
    ) -> None:
        """Update contact info with given label and value."""
        self._run_and_read_output("update", contact_id, field, info_id, label, value)

    def add_info(self, contact_id: str, field: str, label: str, value: str) -> None:
        """Add a contact info."""
        self._run_and_read_output("add", contact_id, field, label, value)

    def delete_info(self, contact_id: str, field: str, info_id: str) -> None:
        """Delete a contact info."""
        self._run_and_read_output("delete", contact_id, field, info_id)

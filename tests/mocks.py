"""Mocks for tests."""


import json
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Iterator

from tests.contact_diff import Mutation


class MockApplescript:
    """Mock object for running applescript code in tests."""

    def __init__(self, test_data_path: Path):
        """Initialize the mock."""
        self._test_data_path = test_data_path
        self._error = False
        self._data: list[dict[Any, Any]] = []
        self._updates: list[Mutation] = []
        self._adds: list[Mutation] = []
        self._deletes: list[Mutation] = []

    def error(self) -> None:
        """Raise an error upon invocation."""
        self._error = True

    def provide(self, *find_data: str) -> None:
        """Specify which test data to find in contacts."""
        self._data = [
            json.loads(
                Path(self._test_data_path / x)
                .with_suffix(".json")
                .read_text(encoding="utf-8")
            )
            for x in find_data
        ]

    def _run_and_read_output(self, script: str, *args: str) -> str:
        """Emulate applescript.run_and_read_output."""
        if self._error:
            raise CalledProcessError(1, "run")
        if script == "find":
            return str(len(self._data))
        if script == "brief":
            brief_data = [
                {
                    "contact_id": x["contact_id"],
                    "name": x["name"],
                    "is_company": x["is_company"],
                }
                for x in self._data
            ]
            return "[\n{}\n]\n".format(
                ",\n".join(json.dumps(x) for x in brief_data if x["contact_id"] in args)
            )
        if script == "detail":
            return "[\n{}\n]\n".format(
                ",\n".join(json.dumps(x) for x in self._data if x["contact_id"] in args)
            )
        if script == "update":
            self._updates.append((*args,))
            return ""
        if script == "add":
            self._adds.append((*args,))
            return ""
        if script == "delete":
            self._deletes.append((*args,))
            return ""
        return ""

    def _run_and_read_log(self, script: str, *args: str) -> Iterator[str]:
        """Emulate applescript.run_and_read_log."""
        if self._error:
            raise CalledProcessError(1, "run")

        if script == "find":
            yield from [x["contact_id"] for x in self._data]

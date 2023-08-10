"""Mocks for tests."""

import json
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Iterator


class MockApplescript:
    """Mock object for running applescript code in tests."""

    def __init__(self, test_data_path: Path):
        """Initialize the mock."""
        self._test_data_path = test_data_path
        self._error = False
        self._data: dict[str, dict[Any, Any]] = {}

    def error(self) -> None:
        """Raise an error upon invocation."""
        self._error = True

    def find(self, *find_data: str) -> None:
        """Specify which test data to find in contacts."""
        data = [
            json.loads(
                Path(self._test_data_path / x)
                .with_suffix(".json")
                .read_text(encoding="utf-8")
            )
            for x in find_data
        ]
        self._data = {x["id"]: x for x in data}

    def run_and_read_output(self, script: str, *args: str) -> str:
        """Emulate applescript.run_and_read_output."""
        if self._error:
            raise CalledProcessError(1, "run")

        if script == "detail":
            return "[\n{}\n]\n".format(
                ",\n".join(json.dumps(self._data[x]) for x in args)
            )
        return ""

    def run_and_read_log(self, script: str, *args: str) -> Iterator[str]:
        """Emulate applescript.run_and_read_log."""
        if self._error:
            raise CalledProcessError(1, "run")

        if script == "find":
            yield from self._data.keys()

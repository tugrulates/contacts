"""Mocks for tests."""

from pathlib import Path
from subprocess import CalledProcessError


class MockApplescript:
    """Mock object for running applescript code in tests."""

    def __init__(self, test_data_path: Path):
        """Initialize the mock."""
        self._test_data_path = test_data_path
        self._error = False
        self._find: list[str] = []

    def error(self) -> None:
        """Raise an error upon invocation."""
        self._error = True

    def find(self, *find_data: str) -> None:
        """Specify which test data to find in contacts."""
        self._find = list(find_data)

    def run(self, script: str, *args: str) -> str:
        """Emulate applescript run."""
        if self._error:
            raise CalledProcessError(1, "run")

        if script == "find":
            return "[\n{}\n]\n".format(
                "\n".join(
                    [
                        Path(self._test_data_path / "{}.yaml".format(x)).read_text(
                            encoding="utf-8"
                        )
                        for x in self._find
                    ]
                )
            )
        return ""

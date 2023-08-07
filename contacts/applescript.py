"""Run applescript code."""

import subprocess  # nosec B404
from pathlib import Path
from typing import Iterator


def run_and_read_output(script: str, *args: str) -> str:
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


def run_and_read_log(script: str, *args: str) -> Iterator[str]:
    """Run a named script with arguments and return the stdout."""
    script_path = (
        Path(__file__).parent / "applescript" / "{}.applescript".format(script)
    )
    try:
        with subprocess.Popen(
            ["/usr/bin/osascript", script_path, *args],
            encoding="utf-8",
            stdout=True,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        ) as process:  # nosec B603
            if process.stderr:
                yield from (x.strip() for x in process.stderr)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise e

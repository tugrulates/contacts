"""Run applescript code."""

import subprocess  # nosec B404
from pathlib import Path


def run(script: str, *args: str) -> str:
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

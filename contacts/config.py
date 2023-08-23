"""Config class."""


from __future__ import annotations

import json
from pathlib import Path

import typer
from pydantic import RootModel
from pydantic.dataclasses import dataclass

CONFIG_PATH = Path(typer.get_app_dir("contacts")) / "config.json"


@dataclass
class Config:
    """App configuration."""

    romanize: str = ""

    def json(self) -> str:
        """Return config as JSON string."""
        return RootModel[Config](self).model_dump_json()

    def dump(self) -> None:
        """Write config to config file."""
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(self.json(), encoding="utf-8")


def get_config() -> Config:
    """Load config from config file."""
    if not CONFIG_PATH.is_file():
        return Config()
    return Config(**dict(json.loads(CONFIG_PATH.read_text(encoding="utf-8"))))

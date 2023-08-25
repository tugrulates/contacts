"""Config class."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from pydantic import BaseModel

from contacts.address import AddressFormat

CONFIG_PATH = Path(typer.get_app_dir("contacts")) / "config.json"


class Config(BaseModel, extra="allow"):
    """App configuration."""

    romanize: Optional[str] = None
    address_formats: dict[str, AddressFormat] = {}
    mapquest_api_key: Optional[str] = None

    def dump(self) -> None:
        """Write config to config file."""
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(
            self.model_dump_json(exclude_defaults=True), encoding="utf-8"
        )


def get_config() -> Config:
    """Load config from config file."""
    if not CONFIG_PATH.is_file():
        return Config()
    return Config.model_validate_json(CONFIG_PATH.read_text(encoding="utf-8"))

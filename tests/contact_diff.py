"""Data diff class to test fixing problems."""


from __future__ import annotations

import dataclasses
from typing import Any, Optional

from contacts.contact import Contact

Mutation = tuple[str, ...]


class ContactDiff:
    """Class that gives the list of mutations to go from one contact to the next."""

    def __init__(self, before: Contact, after: Contact):
        """Initialize the diff."""
        self.updates: list[Mutation] = []
        self.adds: list[Mutation] = []
        self.deletes: list[Mutation] = []
        self._diff(
            dataclasses.asdict(before), dataclasses.asdict(after), (before.contact_id,)
        )

    def _diff(
        self,
        before: dict[str, Any],
        after: dict[str, Any],
        mutation: Mutation,
    ) -> None:
        def _info_dict(
            values: Optional[list[dict[str, Any]]]
        ) -> dict[str, dict[str, Any]]:
            return {
                x["info_id"]: {k: v for k, v in x.items() if k != "info_id"}
                for x in values or []
            }

        for key in before.keys() | after.keys():
            if key in ["contact_id", "name", "is_company", "info_id"]:
                continue
            before_value = before.get(key)
            after_value = after.get(key)
            if isinstance(before_value or after_value, list):
                self._diff(
                    _info_dict(before_value),
                    _info_dict(after_value),
                    (*mutation, key),
                )
            elif isinstance(before_value or after_value, dict):
                self._diff_contact_info(key, before_value, after_value, mutation)
            else:
                self._diff_simple_info(key, before_value, after_value, mutation)

    def _diff_contact_info(
        self,
        field: str,
        before: Optional[dict[str, Any]],
        after: Optional[dict[str, Any]],
        mutation: Mutation,
    ) -> None:
        if (after is None) and (before is not None):
            self.deletes.append((*mutation, field))
        elif (after is not None) and (before is None):
            self.adds.append((*mutation, *after.values()))
        elif (after is not None) and (after != before):
            self.updates.append((*mutation, field, *after.values()))

    def _diff_simple_info(
        self, field: str, before: Any, after: Any, mutation: Mutation
    ) -> None:
        if (after is None) and (before is not None):
            self.deletes.append((*mutation, field))
        elif (after is not None) and (before is None):
            self.adds.append((*mutation, field, str(after)))
        elif (after is not None) and (after != before):
            self.updates.append((*mutation, field, str(after)))

    def __str__(self) -> str:
        """Return formatted diff in string."""
        return (
            "ContactDiff(\n"
            + f"  updates={self.updates}\n"
            + f"  adds={self.adds}\n"
            + f"  deletes={self.deletes}\n"
            + ")"
        )
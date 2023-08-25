"""Data diff class to test fixing problems."""


from __future__ import annotations

from typing import Any, Optional, Union

from contacts.contact import Contact

Mutation = tuple[Union[str, dict[str, str]], ...]


class ContactDiff:
    """Class that gives the list of mutations to go from one contact to the next."""

    def __init__(self, before: Contact, after: Contact):
        """Initialize the diff."""
        self.updates: list[Mutation] = []
        self.adds: list[Mutation] = []
        self.deletes: list[Mutation] = []
        self._diff(before.model_dump(), after.model_dump(), (before.id,))

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
                x["id"]: {
                    k: str(v) for k, v in x.items() if k != "id" and v is not None
                }
                for x in values or []
            }

        for key in before.keys() | after.keys():
            if key in ["id", "name", "is_company", "id"]:
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
        before: Optional[dict[str, str]],
        after: Optional[dict[str, str]],
        mutation: Mutation,
    ) -> None:
        if (after is None) and (before is not None):
            self.deletes.append((*mutation, field))
        elif (after is not None) and (before is None):
            self.adds.append((*mutation, after))
        elif (after is not None) and (before is not None) and (after != before):
            values = {k: v for k, v in after.items() if v != before.get(k)}
            self.updates.append((*mutation, field, values))

    def _diff_simple_info(
        self, field: str, before: Any, after: Any, mutation: Mutation
    ) -> None:
        if (after is None) and (before is not None):
            self.deletes.append((*mutation, field))
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

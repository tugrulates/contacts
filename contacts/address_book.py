"""AddressBook abstract base class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterator, Optional, Protocol

if TYPE_CHECKING:
    from contacts.contact import Contact


class AddressBook(ABC):
    """An address book that fetches and updates contacts."""

    @abstractmethod
    def count(self, keywords: list[str]) -> int:
        """Return number of contacts matching given keywords."""

    @abstractmethod
    def find(self, keywords: list[str]) -> Iterator[Contact]:
        """Return list of contact ids matching given keywords."""

    @abstractmethod
    def get(self, contact_id: str) -> Contact:
        """Fetch a contact with its id."""

    @abstractmethod
    def _update_field(self, contact_id: str, field: str, value: str) -> None:
        """Add or update a contact field with given value."""

    @abstractmethod
    def _delete_field(self, contact_id: str, field: str) -> None:
        """Delete a contact field."""

    @abstractmethod
    def _update_info(
        self, contact_id: str, field: str, info_id: str, **values: str
    ) -> None:
        """Update a contact info with given label and value."""

    @abstractmethod
    def _add_info(self, contact_id: str, field: str, **values: str) -> None:
        """Add a contact info."""

    @abstractmethod
    def _delete_info(self, contact_id: str, field: str, info_id: str) -> None:
        """Delete a contact info."""

    def update_prefix(self, contact_id: str, value: str) -> None:
        """Add or update a contact prefix."""
        self._update_field(contact_id, "prefix", value)

    def delete_prefix(self, contact_id: str) -> None:
        """Delete a contact prefix."""
        self._delete_field(contact_id, "prefix")

    def update_first_name(self, contact_id: str, value: str) -> None:
        """Add or update a contact first_name."""
        self._update_field(contact_id, "first_name", value)

    def delete_first_name(self, contact_id: str) -> None:
        """Delete a contact first_name."""
        self._delete_field(contact_id, "first_name")

    def update_phonetic_first_name(self, contact_id: str, value: str) -> None:
        """Add or update a contact phonetic_first_name."""
        self._update_field(contact_id, "phonetic_first_name", value)

    def delete_phonetic_first_name(self, contact_id: str) -> None:
        """Delete a contact phonetic_first_name."""
        self._delete_field(contact_id, "phonetic_first_name")

    def update_middle_name(self, contact_id: str, value: str) -> None:
        """Add or update a contact middle_name."""
        self._update_field(contact_id, "middle_name", value)

    def delete_middle_name(self, contact_id: str) -> None:
        """Delete a contact middle_name."""
        self._delete_field(contact_id, "middle_name")

    def update_phonetic_middle_name(self, contact_id: str, value: str) -> None:
        """Add or update a contact phonetic_middle_name."""
        self._update_field(contact_id, "phonetic_middle_name", value)

    def delete_phonetic_middle_name(self, contact_id: str) -> None:
        """Delete a contact phonetic middle name."""
        self._delete_field(contact_id, "phonetic_middle_name")

    def update_last_name(self, contact_id: str, value: str) -> None:
        """Add or update a contact last_name."""
        self._update_field(contact_id, "last_name", value)

    def delete_last_name(self, contact_id: str) -> None:
        """Delete a contact last name."""
        self._delete_field(contact_id, "last_name")

    def update_phonetic_last_name(self, contact_id: str, value: str) -> None:
        """Add or update a contact phonetic_last_name."""
        self._update_field(contact_id, "phonetic_last_name", value)

    def delete_phonetic_last_name(self, contact_id: str) -> None:
        """Delete a contact phonetic last name."""
        self._delete_field(contact_id, "phonetic_last_name")

    def update_maiden_name(self, contact_id: str, value: str) -> None:
        """Add or update a contact maiden_name."""
        self._update_field(contact_id, "maiden_name", value)

    def delete_maiden_name(self, contact_id: str) -> None:
        """Delete a contact maiden name."""
        self._delete_field(contact_id, "maiden_name")

    def update_suffix(self, contact_id: str, value: str) -> None:
        """Add or update a contact suffix."""
        self._update_field(contact_id, "suffix", value)

    def delete_suffix(self, contact_id: str) -> None:
        """Delete a contact suffix."""
        self._delete_field(contact_id, "suffix")

    def update_nickname(self, contact_id: str, value: str) -> None:
        """Add or update a contact nickname."""
        self._update_field(contact_id, "nickname", value)

    def delete_nickname(self, contact_id: str) -> None:
        """Delete a contact nickname."""
        self._delete_field(contact_id, "nickname")

    def update_job_title(self, contact_id: str, value: str) -> None:
        """Add or update a contact job_title."""
        self._update_field(contact_id, "job_title", value)

    def delete_job_title(self, contact_id: str) -> None:
        """Delete a contact job title."""
        self._delete_field(contact_id, "job_title")

    def update_department(self, contact_id: str, value: str) -> None:
        """Add or update a contact department."""
        self._update_field(contact_id, "department", value)

    def delete_department(self, contact_id: str) -> None:
        """Delete a contact department."""
        self._delete_field(contact_id, "department")

    def update_organization(self, contact_id: str, value: str) -> None:
        """Add or update a contact organization."""
        self._update_field(contact_id, "organization", value)

    def delete_organization(self, contact_id: str) -> None:
        """Delete a contact organization."""
        self._delete_field(contact_id, "organization")

    def update_phone(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """Update a contact phone."""
        self._update_info(
            contact_id,
            "phones",
            info_id,
            **self.__optional_values(label=label, value=value),
        )

    def add_phone(self, contact_id: str, label: str, value: str) -> None:
        """Add a contact phone."""
        self._add_info(contact_id, "phones", label=label, value=value)

    def delete_phone(self, contact_id: str, info_id: str) -> None:
        """Delete a contact phone."""
        self._delete_info(contact_id, "phones", info_id)

    def update_email(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """Update a contact email."""
        self._update_info(
            contact_id,
            "emails",
            info_id,
            **self.__optional_values(label=label, value=value),
        )

    def add_email(
        self,
        contact_id: str,
        label: str,
        value: str,
    ) -> None:
        """Add a contact e-mail."""
        self._add_info(contact_id, "emails", label=label, value=value)

    def delete_email(self, contact_id: str, info_id: str) -> None:
        """Delete a contact e-mail."""
        self._delete_info(contact_id, "emails", info_id)

    def update_home_page(self, contact_id: str, value: str) -> None:
        """Add or update a contact home_page."""
        self._update_field(contact_id, "home_page", value)

    def delete_home_page(self, contact_id: str) -> None:
        """Delete a contact home page."""
        self._delete_field(contact_id, "home_page")

    def update_url(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """Update a contact URL."""
        self._update_info(
            contact_id,
            "urls",
            info_id,
            **self.__optional_values(label=label, value=value),
        )

    def add_url(self, contact_id: str, label: str, value: str) -> None:
        """Add a contact URL."""
        self._add_info(contact_id, "urls", label=label, value=value)

    def delete_url(self, contact_id: str, info_id: str) -> None:
        """Delete a contact URL."""
        self._delete_info(contact_id, "urls", info_id)

    def update_address(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        country_code: Optional[str] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
    ) -> None:
        """Update a contact address."""
        self._update_info(
            contact_id,
            "addresses",
            info_id,
            **self.__optional_values(
                label=label,
                country_code=country_code,
                street=street,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country,
            ),
        )

    def add_address(
        self,
        contact_id: str,
        label: str,
        *,
        country_code: Optional[str] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
    ) -> None:
        """Add a contact address."""
        self._add_info(
            contact_id,
            "addresses",
            label=label,
            **self.__optional_values(
                country_code=country_code,
                street=street,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country,
            ),
        )

    def delete_address(self, contact_id: str, info_id: str) -> None:
        """Delete a contact address."""
        self._delete_info(contact_id, "addresses", info_id)

    def update_birth_date(self, contact_id: str, value: str) -> None:
        """Add or update a contact birth date."""
        self._update_field(contact_id, "birth_date", value)

    def delete_birth_date(self, contact_id: str) -> None:
        """Delete a contact birth date."""
        self._delete_field(contact_id, "birth_date")

    def update_custom_date(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """Update a contact custom date."""
        self._update_info(
            contact_id,
            "custom_dates",
            info_id,
            **self.__optional_values(label=label, value=value),
        )

    def add_custom_date(self, contact_id: str, label: str, value: str) -> None:
        """Add a contact custom date."""
        self._add_info(contact_id, "custom_dates", label=label, value=value)

    def delete_custom_date(self, contact_id: str, info_id: str) -> None:
        """Delete a contact custom date."""
        self._delete_info(contact_id, "custom_dates", info_id)

    def update_related_name(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """Update a contact related name."""
        self._update_info(
            contact_id,
            "related_names",
            info_id,
            **self.__optional_values(label=label, value=value),
        )

    def add_related_name(self, contact_id: str, label: str, value: str) -> None:
        """Add a contact related name."""
        self._add_info(contact_id, "related_names", label=label, value=value)

    def delete_related_name(self, contact_id: str, info_id: str) -> None:
        """Delete a contact related name."""
        self._delete_info(contact_id, "related_names", info_id)

    def update_social_profile(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        value: Optional[str] = None,
        user_identifier: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        """Update a contact social profile."""
        self._update_info(
            contact_id,
            "social_profiles",
            info_id,
            **self.__optional_values(
                label=label, value=value, user_identifier=user_identifier, url=url
            ),
        )

    def add_social_profile(
        self,
        contact_id: str,
        label: str,
        value: str,
        *,
        user_identifier: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        """Add a contact social profile."""
        self._add_info(
            contact_id,
            "social_profiles",
            label=label,
            value=value,
            **self.__optional_values(user_identifier=user_identifier, url=url),
        )

    def delete_social_profile(self, contact_id: str, info_id: str) -> None:
        """Delete a contact social profile."""
        self._delete_info(contact_id, "social_profiles", info_id)

    def update_instant_message(
        self,
        contact_id: str,
        info_id: str,
        *,
        label: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        """Update a contact instant_messages."""
        self._update_info(
            contact_id,
            "instant_messages",
            info_id,
            **self.__optional_values(label=label, value=value),
        )

    def add_instant_message(self, contact_id: str, label: str, value: str) -> None:
        """Add a contact instant message."""
        self._add_info(
            contact_id,
            "instant_messages",
            label=label,
            value=value,
        )

    def delete_instant_message(self, contact_id: str, info_id: str) -> None:
        """Delete a contact instant message."""
        self._delete_info(contact_id, "instant_messages", info_id)

    def update_note(self, contact_id: str, value: str) -> None:
        """Add or update a contact note."""
        self._update_field(contact_id, "note", value)

    def delete_note(self, contact_id: str) -> None:
        """Delete a contact note."""
        self._delete_field(contact_id, "note")

    def __optional_values(self, **values: Optional[str]) -> dict[str, str]:
        return {k: v for k, v in values.items() if v is not None}

    class UpdateFieldFunction(Protocol):
        """Type hint for update field calls."""

        def __call__(  # noqa: D102
            self,
            __address_book: AddressBook,
            contact_id: str,
            value: str,
        ) -> None:
            ...

    class DeleteFieldFunction(Protocol):
        """Type hint for delete field calls."""

        def __call__(  # noqa: D102
            self,
            __address_book: AddressBook,
            contact_id: str,
        ) -> None:
            ...

    class UpdateInfoLabelFunction(Protocol):
        """Type hint for update info calls for labels."""

        def __call__(  # noqa: D102
            self,
            __address_book: AddressBook,
            contact_id: str,
            info_id: str,
            *,
            label: Optional[str],
        ) -> None:
            ...

    class DeleteInfoFunction(Protocol):
        """Type hint for delete info calls."""

        def __call__(  # noqa: D102
            self,
            __address_book: AddressBook,
            contact_id: str,
            info_id: str,
        ) -> None:
            ...

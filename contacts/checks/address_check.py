"""AddressCheck class."""

from __future__ import annotations

from functools import partial
from itertools import chain
from typing import Optional

import isocodes

from contacts import address, config
from contacts.address import AddressFormat, SemanticAddressField
from contacts.address_book import AddressBook
from contacts.contact import Contact, ContactAddress
from contacts.problem import Check, Problem


class AddressCheck(Check):
    """Checker for addresses."""

    def __init__(self) -> None:
        """Initialize with config."""
        self._config = config.get_config()
        self._geocoder = address.get_geocoder()

    def check(self, contact: Contact) -> list[Problem]:
        """Check contact."""

        def display(address: ContactAddress) -> str:
            return address.value.replace("\n", " ")

        def check_values(address: ContactAddress) -> list[Problem]:
            address_format = get_address_format(address)
            problems = []

            if address_format.street and not address.street:
                problems.append(Problem(f"Street for '{display(address)}' is missing."))
            if address_format.city and not address.city:
                problems.append(Problem(f"City for '{display(address)}' is missing."))
            if address_format.state and not address.state:
                problems.append(Problem(f"State for '{display(address)}' is missing."))
            if address_format.zip_code and not address.zip_code:
                problems.append(
                    Problem(f"ZIP code for '{display(address)}' is missing.")
                )

            if not address_format.street and address.street:
                problems.append(
                    Problem(
                        f"Street '{address.street}' should be removed.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            street="",
                        ),
                    )
                )
            if not address_format.city and address.city:
                problems.append(
                    Problem(
                        f"City '{address.city}' should be removed.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            city="",
                        ),
                    )
                )
            if not address_format.state and address.state:
                problems.append(
                    Problem(
                        f"State '{address.state}' should be removed.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            state="",
                        ),
                    )
                )
            if not address_format.zip_code and address.zip_code:
                problems.append(
                    Problem(
                        f"ZIP code '{address.zip_code}' should be removed.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            zip_code="",
                        ),
                    )
                )

            return problems

        def check_country(address: ContactAddress) -> Optional[Problem]:
            _, formatted = find_country(address)
            if not formatted:
                if not address.country:
                    return Problem(f"Country for '{display(address)}' is missing.")
                return Problem(f"Country '{address.country}' is invalid.")

            if not address.country:
                return Problem(
                    f"Country for '{display(address)}' should be '{formatted}'.",
                    fix=partial(
                        AddressBook.update_address,
                        contact_id=contact.id,
                        info_id=address.id,
                        country=formatted,
                    ),
                )
            if address.country != formatted:
                return Problem(
                    f"Country '{address.country}' should be '{formatted}'.",
                    fix=partial(
                        AddressBook.update_address,
                        contact_id=contact.id,
                        info_id=address.id,
                        country=formatted,
                    ),
                )
            return None

        def check_country_code(address: ContactAddress) -> Optional[Problem]:
            formatted, _ = find_country(address)
            if not formatted:
                if not address.country:
                    return None
                if not address.country_code:
                    return Problem(f"Country code for '{display(address)}' is missing.")
                return Problem(f"Country code '{address.country_code}' is invalid.")

            if not address.country_code:
                return Problem(
                    f"Country code for '{display(address)}' should be '{formatted}'.",
                    fix=partial(
                        AddressBook.update_address,
                        contact_id=contact.id,
                        info_id=address.id,
                        country_code=formatted,
                    ),
                )
            if address.country_code != formatted:
                return Problem(
                    f"Country code '{address.country_code}' should be '{formatted}'.",
                    fix=partial(
                        AddressBook.update_address,
                        contact_id=contact.id,
                        info_id=address.id,
                        country_code=formatted,
                    ),
                )
            return None

        def find_country(
            address: ContactAddress,
        ) -> tuple[Optional[str], Optional[str]]:
            found = None
            if address.country_code:
                found = isocodes.countries.get(alpha_2=address.country_code.upper())
            elif address.country:
                found = isocodes.countries.get(name=address.country)
            if not found:
                return (None, None)
            return (found["alpha_2"].lower(), found["name"])

        def check_geocode(address: ContactAddress) -> list[Problem]:
            address_format = get_address_format(address)
            if not address_format or not self._geocoder:
                return []

            geo = self._geocoder.geocode(address)
            if not geo:
                return [Problem(f"Address '{display(address)}' cannot be geocoded.")]

            problems = []

            geo_street, geo_city, geo_state, geo_zip_code = (
                address_format.street_from_geocode(geo),
                address_format.city_from_geocode(geo),
                address_format.state_from_geocode(geo),
                address_format.zip_code_from_geocode(geo),
            )

            street_lines = address.street.split("\n") if address.street else [None]
            if geo_street and street_lines[0] != geo_street:
                geo_street = "\n".join(filter(None, (geo_street, *street_lines[1:])))
                problems.append(
                    Problem(
                        f"Street '{address.street}' should be '{geo_street}'.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            street=geo_street,
                        ),
                    )
                )

            if geo_city and address.city != geo_city:
                problems.append(
                    Problem(
                        f"City '{address.city}' should be '{geo_city}'.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            city=geo_city,
                        ),
                    )
                )

            if geo_state and address.state != geo_state:
                problems.append(
                    Problem(
                        f"State '{address.state}' should be '{geo_state}'.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            state=geo_state,
                        ),
                    )
                )

            if geo_zip_code and address.zip_code != geo_zip_code:
                problems.append(
                    Problem(
                        f"ZIP code '{address.zip_code}' should be '{geo_zip_code}'.",
                        fix=partial(
                            AddressBook.update_address,
                            contact_id=contact.id,
                            info_id=address.id,
                            zip_code=geo_zip_code,
                        ),
                    )
                )

            return problems

        def get_address_format(address: ContactAddress) -> AddressFormat:
            return self._config.address_formats.get(
                address.country_code or "",
                AddressFormat(
                    street=SemanticAddressField.STREET,
                    city=SemanticAddressField.CITY,
                    state=SemanticAddressField.STATE,
                    zip_code=SemanticAddressField.ZIP_CODE,
                ),
            )

        problems = chain(
            *(check_values(address) for address in contact.addresses),
            *(check_geocode(address) for address in contact.addresses),
            (check_country_code(address) for address in contact.addresses),
            (check_country(address) for address in contact.addresses),
        )
        return [x for x in problems if x]

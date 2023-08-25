"""Address parsing and validation related classes."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import MapQuest
from geopy.location import Location
from pydantic import BaseModel

from contacts.contact import ContactAddress


class SemanticAddressField(str, Enum):
    """Semantic address field that maps to MapQuest result fields."""

    STREET = "street"
    NEIGHBORHOOD = "neigborhood"
    CITY = "city"
    COUNTY = "county"
    STATE = "state"
    ZIP_CODE = "zip_code"
    COUNTRY = "country"


class Geocode(BaseModel):
    """Geocode of an address."""

    street: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = None


class AddressFormat(BaseModel):
    """Address formats for a country."""

    street: Optional[SemanticAddressField] = None
    city: Optional[SemanticAddressField] = None
    state: Optional[SemanticAddressField] = None
    zip_code: Optional[SemanticAddressField] = None

    def street_from_geocode(self, geocode: Geocode) -> Optional[str]:
        """Get street from geocode for this format."""
        return geocode.model_dump()[self.street.value] if self.street else None

    def city_from_geocode(self, geocode: Geocode) -> Optional[str]:
        """Get city from geocode for this format."""
        return geocode.model_dump()[self.city.value] if self.city else None

    def state_from_geocode(self, geocode: Geocode) -> Optional[str]:
        """Get state from geocode for this format."""
        return geocode.model_dump()[self.state.value] if self.state else None

    def zip_code_from_geocode(self, geocode: Geocode) -> Optional[str]:
        """Get zip code from geocode for this format."""
        return geocode.model_dump()[self.zip_code.value] if self.zip_code else None


class Geocoder(ABC):
    """Geocoder service."""

    @abstractmethod
    def geocode(self, address: ContactAddress) -> Optional[Geocode]:
        """Geolocate address."""


class MapQuestGeocoder(Geocoder):
    """MapQuest geocoding service."""

    MAPQUEST_FIELDS: dict[SemanticAddressField, str] = {
        SemanticAddressField.STREET: "street",
        SemanticAddressField.NEIGHBORHOOD: "Neighborhood",
        SemanticAddressField.CITY: "City",
        SemanticAddressField.COUNTY: "County",
        SemanticAddressField.STATE: "State",
        SemanticAddressField.ZIP_CODE: "postalCode",
        SemanticAddressField.COUNTRY: "Country",
    }

    def __init__(self, api_key: str) -> None:
        """Initialize."""
        self._geocode = RateLimiter(
            MapQuest(api_key=api_key).geocode, min_delay_seconds=1
        )

    def geocode(self, address: ContactAddress) -> Optional[Geocode]:
        """Geocode address."""
        geo: Optional[Location] = self._geocode(address.value)
        if not geo:
            return None
        return Geocode(
            street=self._raw_value(geo, SemanticAddressField.STREET),
            neighborhood=self._raw_value(geo, SemanticAddressField.NEIGHBORHOOD),
            city=self._raw_value(geo, SemanticAddressField.CITY),
            county=self._raw_value(geo, SemanticAddressField.COUNTY),
            state=self._raw_value(geo, SemanticAddressField.STATE),
            zip_code=self._raw_value(geo, SemanticAddressField.ZIP_CODE),
            country_code=self._raw_value(geo, SemanticAddressField.COUNTRY),
        )

    def _raw_value(
        self, geo: Location, field: Optional[SemanticAddressField]
    ) -> Optional[str]:
        if field is None:
            return None
        geo_raw: dict[str, str] = geo.raw
        key = MapQuestGeocoder.MAPQUEST_FIELDS[field]
        value = geo_raw.get(key)
        if value:
            return value
        for index in range(1, 10):
            if geo_raw.get(f"adminArea{index}Type") == key:
                value = geo_raw.get(f"adminArea{index}")
                if value:
                    return value
        return None


def get_geocoder() -> Optional[Geocoder]:
    """Return a geocoder implementation using MapQuest API."""
    from contacts.config import get_config

    config = get_config()
    if config.mapquest_api_key is None:
        return None
    return MapQuestGeocoder(config.mapquest_api_key)

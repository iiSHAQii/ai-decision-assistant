import logging
from typing import Protocol

import requests

from backend.services.providers.base import DataPoint, DataProvider, Direction
from backend.services.providers.geocoding import OpenMeteoGeocoder
from backend.services.providers.iso_country_codes import ISO2_TO_ISO3

log = logging.getLogger(__name__)

WORLD_BANK_URL_TEMPLATE = (
    "https://api.worldbank.org/v2/country/{iso3}/indicator/{indicator}"
)
DEFAULT_TIMEOUT = 5.0
LOOKBACK_YEARS = 8  # how far back to scan for the most recent non-null value


class _HttpSession(Protocol):
    def get(self, url: str, params: dict | None = ..., timeout: float | None = ...): ...


class WorldBankProvider(DataProvider):
    """Country-level indicators from the World Bank Open Data API.

    Resolves an option (e.g. a city) to a country via the geocoder, maps the
    ISO-2 country code to ISO-3, then queries the World Bank for the most
    recent non-null value of `indicator`. Display format defaults to
    "<value> (<ISO3>, <year>)".

    Returns None when:
      - geocoding finds no match for the option
      - the resolved country isn't in ISO2_TO_ISO3 (warning logged)
      - the World Bank has no recent data for this country/indicator

    Raises on network errors, HTTP errors, and malformed responses.
    """

    def __init__(
        self,
        criterion: str,
        indicator: str,
        direction: Direction,
        unit: str = "",
        geocoder: OpenMeteoGeocoder | None = None,
        session: _HttpSession | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.criterion = criterion
        self.direction = direction
        self._indicator = indicator
        self._unit = unit
        self._session = session or requests.Session()
        self._timeout = timeout
        self._geocoder = geocoder or OpenMeteoGeocoder(
            session=session, timeout=timeout
        )

    def _fetch_indicator(self, iso3: str) -> tuple[float, int] | None:
        """Return (value, year) for the most recent non-null observation, or None."""
        url = WORLD_BANK_URL_TEMPLATE.format(iso3=iso3, indicator=self._indicator)
        try:
            resp = self._session.get(
                url,
                params={
                    "format": "json",
                    "per_page": LOOKBACK_YEARS,
                    "mrnev": LOOKBACK_YEARS,  # most recent non-empty values
                },
                timeout=self._timeout,
            )
            resp.raise_for_status()
            payload = resp.json()
        except (requests.RequestException, ValueError) as e:
            log.warning(
                "World Bank request failed for %s/%s: %s", iso3, self._indicator, e
            )
            raise

        # World Bank returns [metadata, [observations...]]
        if not isinstance(payload, list) or len(payload) < 2:
            raise ValueError(
                f"Unexpected World Bank payload shape for {iso3}/{self._indicator}: "
                f"{type(payload).__name__}"
            )
        rows = payload[1]
        if not isinstance(rows, list):
            return None

        for row in rows:
            value = row.get("value")
            if value is None:
                continue
            try:
                return float(value), int(row["date"])
            except (KeyError, TypeError, ValueError) as e:
                log.warning(
                    "Malformed World Bank row for %s/%s: %s", iso3, self._indicator, e
                )
                raise
        return None

    def _format_display(self, value: float, year: int, iso3: str) -> str:
        if self._unit:
            return f"{value:,.0f} {self._unit} ({iso3}, {year})"
        return f"{value:,.2f} ({iso3}, {year})"

    def fetch(self, option_name: str) -> DataPoint | None:
        geo = self._geocoder.lookup(option_name)
        if geo is None:
            return None

        iso3 = ISO2_TO_ISO3.get(geo.country_code)
        if iso3 is None:
            log.warning(
                "No ISO-3 mapping for country code %r (option %r) — "
                "extend ISO2_TO_ISO3 to cover this country.",
                geo.country_code,
                option_name,
            )
            return None

        observation = self._fetch_indicator(iso3)
        if observation is None:
            return None

        value, year = observation
        return DataPoint(
            raw_value=value,
            display_value=self._format_display(value, year, iso3),
            source="worldbank",
        )

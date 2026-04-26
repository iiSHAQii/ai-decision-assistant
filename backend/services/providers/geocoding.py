import logging
from dataclasses import dataclass
from typing import Protocol

import requests

log = logging.getLogger(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
DEFAULT_TIMEOUT = 5.0


class _HttpSession(Protocol):
    def get(self, url: str, params: dict | None = ..., timeout: float | None = ...): ...


@dataclass(frozen=True)
class GeoResult:
    latitude: float
    longitude: float
    country_code: str  # ISO 3166-1 alpha-2 (e.g. "GB", "DE")


class OpenMeteoGeocoder:
    """Resolves a free-text place name to lat/lon and country via Open-Meteo.

    Returns None when the API succeeds but finds no match (legitimate miss).
    Network errors, HTTP errors, and malformed payloads are logged and re-raised.
    """

    def __init__(
        self,
        session: _HttpSession | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self._session = session or requests.Session()
        self._timeout = timeout

    def lookup(self, name: str) -> GeoResult | None:
        try:
            resp = self._session.get(
                GEOCODING_URL,
                params={
                    "name": name,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
                timeout=self._timeout,
            )
            resp.raise_for_status()
            payload = resp.json()
        except (requests.RequestException, ValueError) as e:
            log.warning("Geocoding request failed for %r: %s", name, e)
            raise

        results = payload.get("results") or []
        if not results:
            return None

        first = results[0]
        try:
            return GeoResult(
                latitude=float(first["latitude"]),
                longitude=float(first["longitude"]),
                country_code=str(first["country_code"]).upper(),
            )
        except (KeyError, TypeError, ValueError) as e:
            log.warning("Malformed geocoding response for %r: %s", name, e)
            raise

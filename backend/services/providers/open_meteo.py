import logging
from typing import Protocol

import requests

from backend.services.providers.base import DataPoint, DataProvider, Direction

log = logging.getLogger(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
IDEAL_TEMP_C = 21.0
DEFAULT_TIMEOUT = 5.0


class _HttpSession(Protocol):
    def get(self, url: str, params: dict | None = ..., timeout: float | None = ...): ...


class OpenMeteoWeatherProvider(DataProvider):
    """Weather 'comfort' score from Open-Meteo (no auth required).

    Pipeline per option:
      1. Geocode the option name -> (lat, lon).
      2. Fetch a 7-day daily forecast for that location.
      3. Compute a comfort score from the mean temperature, where higher is better:
         comfort = 100 - |mean_temp - 21°C|.

    Returns None when geocoding finds no match for the option (legitimate miss).
    Raises on network errors, HTTP errors, and malformed responses — these are
    surfaced rather than swallowed so they don't masquerade as missing data.
    """

    criterion: str = "weather"
    direction: Direction = "higher_is_better"

    def __init__(
        self,
        session: _HttpSession | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self._session = session or requests.Session()
        self._timeout = timeout

    def _geocode(self, option_name: str) -> tuple[float, float] | None:
        resp = self._session.get(
            GEOCODING_URL,
            params={
                "name": option_name,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=self._timeout,
        )
        resp.raise_for_status()
        payload = resp.json()
        results = payload.get("results") or []
        if not results:
            return None
        first = results[0]
        return float(first["latitude"]), float(first["longitude"])

    def _fetch_daily_temps(self, lat: float, lon: float) -> tuple[list[float], list[float]]:
        resp = self._session.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min",
                "forecast_days": 7,
                "timezone": "auto",
            },
            timeout=self._timeout,
        )
        resp.raise_for_status()
        daily = resp.json().get("daily") or {}
        highs = daily.get("temperature_2m_max")
        lows = daily.get("temperature_2m_min")
        if not isinstance(highs, list) or not isinstance(lows, list) or not highs or not lows:
            raise ValueError(
                f"Open-Meteo forecast returned no daily temperatures for ({lat}, {lon})"
            )
        return [float(h) for h in highs], [float(l) for l in lows]

    def fetch(self, option_name: str) -> DataPoint | None:
        try:
            coords = self._geocode(option_name)
        except (requests.RequestException, ValueError, KeyError) as e:
            log.warning("Open-Meteo geocoding failed for %r: %s", option_name, e)
            raise

        if coords is None:
            return None  # legitimate "no data" — not an error

        try:
            highs, lows = self._fetch_daily_temps(*coords)
        except (requests.RequestException, ValueError, KeyError) as e:
            log.warning(
                "Open-Meteo forecast failed for %r at %s: %s", option_name, coords, e
            )
            raise

        mean_temp = (sum(highs) / len(highs) + sum(lows) / len(lows)) / 2
        comfort = 100.0 - abs(mean_temp - IDEAL_TEMP_C)
        return DataPoint(
            raw_value=comfort,
            display_value=f"{mean_temp:.1f}°C avg (next 7 days)",
            source="open-meteo",
        )

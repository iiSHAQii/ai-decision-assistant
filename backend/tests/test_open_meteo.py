import unittest
from unittest.mock import MagicMock

import requests

from backend.services.providers.geocoding import GEOCODING_URL
from backend.services.providers.open_meteo import (
    FORECAST_URL,
    IDEAL_TEMP_C,
    OpenMeteoWeatherProvider,
)


def _response(json_data, status: int = 200):
    """Build a mock requests.Response-like object."""
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    if status >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(f"status {status}")
    else:
        resp.raise_for_status.return_value = None
    return resp


def _session_returning(*responses):
    session = MagicMock()
    session.get.side_effect = list(responses)
    return session


def _geocode_payload(lat: float, lon: float, cc: str = "GB") -> dict:
    return {"results": [{"latitude": lat, "longitude": lon, "country_code": cc}]}


class TestOpenMeteoWeatherProvider(unittest.TestCase):
    def test_returns_comfort_datapoint_on_happy_path(self):
        # Highs around 23, lows around 19 -> mean 21 -> comfort = 100.
        geocode_resp = _response(_geocode_payload(51.5, -0.1))
        forecast_resp = _response(
            {
                "daily": {
                    "temperature_2m_max": [23.0] * 7,
                    "temperature_2m_min": [19.0] * 7,
                }
            }
        )
        session = _session_returning(geocode_resp, forecast_resp)
        provider = OpenMeteoWeatherProvider(session=session)

        result = provider.fetch("London")

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.raw_value, 100.0)
        self.assertIn("21.0°C", result.display_value)
        self.assertEqual(result.source, "open-meteo")

    def test_comfort_decreases_with_distance_from_ideal(self):
        geocode_resp = _response(_geocode_payload(0.0, 0.0))
        # mean = 31°C -> comfort = 100 - |31 - 21| = 90
        forecast_resp = _response(
            {
                "daily": {
                    "temperature_2m_max": [33.0] * 7,
                    "temperature_2m_min": [29.0] * 7,
                }
            }
        )
        session = _session_returning(geocode_resp, forecast_resp)
        provider = OpenMeteoWeatherProvider(session=session)

        result = provider.fetch("Hot City")
        self.assertAlmostEqual(result.raw_value, 100.0 - abs(31.0 - IDEAL_TEMP_C))

    def test_returns_none_when_geocoding_finds_no_match(self):
        # Empty results = legitimate "city not found", not an error.
        session = _session_returning(_response({"results": []}))
        provider = OpenMeteoWeatherProvider(session=session)

        self.assertIsNone(provider.fetch("Atlantis"))
        # Forecast should NOT have been called.
        self.assertEqual(session.get.call_count, 1)

    def test_geocoding_http_error_propagates(self):
        session = _session_returning(_response({}, status=500))
        provider = OpenMeteoWeatherProvider(session=session)

        with self.assertRaises(requests.HTTPError):
            provider.fetch("London")

    def test_forecast_http_error_propagates(self):
        geocode_resp = _response(_geocode_payload(51.5, -0.1))
        session = _session_returning(geocode_resp, _response({}, status=503))
        provider = OpenMeteoWeatherProvider(session=session)

        with self.assertRaises(requests.HTTPError):
            provider.fetch("London")

    def test_network_error_propagates(self):
        session = MagicMock()
        session.get.side_effect = requests.ConnectionError("boom")
        provider = OpenMeteoWeatherProvider(session=session)

        with self.assertRaises(requests.ConnectionError):
            provider.fetch("London")

    def test_malformed_geocode_response_raises(self):
        session = _session_returning(_response({"results": [{"name": "Nowhere"}]}))
        provider = OpenMeteoWeatherProvider(session=session)

        with self.assertRaises(KeyError):
            provider.fetch("Nowhere")

    def test_empty_forecast_arrays_raise_value_error(self):
        geocode_resp = _response(_geocode_payload(0.0, 0.0))
        forecast_resp = _response(
            {"daily": {"temperature_2m_max": [], "temperature_2m_min": []}}
        )
        session = _session_returning(geocode_resp, forecast_resp)
        provider = OpenMeteoWeatherProvider(session=session)

        with self.assertRaises(ValueError):
            provider.fetch("Somewhere")

    def test_geocoding_called_with_expected_params(self):
        geocode_resp = _response(_geocode_payload(1.0, 2.0))
        forecast_resp = _response(
            {
                "daily": {
                    "temperature_2m_max": [20.0],
                    "temperature_2m_min": [20.0],
                }
            }
        )
        session = _session_returning(geocode_resp, forecast_resp)
        provider = OpenMeteoWeatherProvider(session=session)

        provider.fetch("Berlin")

        first_call = session.get.call_args_list[0]
        self.assertEqual(first_call.args[0], GEOCODING_URL)
        self.assertEqual(first_call.kwargs["params"]["name"], "Berlin")

        second_call = session.get.call_args_list[1]
        self.assertEqual(second_call.args[0], FORECAST_URL)
        self.assertEqual(second_call.kwargs["params"]["latitude"], 1.0)
        self.assertEqual(second_call.kwargs["params"]["longitude"], 2.0)


if __name__ == "__main__":
    unittest.main()

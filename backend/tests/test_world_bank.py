import unittest
from unittest.mock import MagicMock

import requests

from backend.services.providers.geocoding import GeoResult, OpenMeteoGeocoder
from backend.services.providers.world_bank import (
    WORLD_BANK_URL_TEMPLATE,
    WorldBankProvider,
)


def _response(json_data, status: int = 200):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    if status >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(f"status {status}")
    else:
        resp.raise_for_status.return_value = None
    return resp


def _wb_payload(observations: list[tuple[float | None, str]]) -> list:
    """Build a fake World Bank payload: [metadata, [rows...]]."""
    rows = [{"value": v, "date": d} for v, d in observations]
    return [{"page": 1, "pages": 1, "total": len(rows)}, rows]


def _fake_geocoder(result: GeoResult | None) -> MagicMock:
    g = MagicMock(spec=OpenMeteoGeocoder)
    g.lookup.return_value = result
    return g


class TestWorldBankProvider(unittest.TestCase):
    def _provider(self, geocoder, session=None):
        return WorldBankProvider(
            criterion="salary",
            indicator="NY.GDP.PCAP.CD",
            direction="higher_is_better",
            unit="USD/yr",
            geocoder=geocoder,
            session=session or MagicMock(),
        )

    def test_returns_datapoint_on_happy_path(self):
        geocoder = _fake_geocoder(
            GeoResult(latitude=51.5, longitude=-0.1, country_code="GB")
        )
        wb_resp = _response(_wb_payload([(48000.0, "2022")]))
        session = MagicMock()
        session.get.return_value = wb_resp

        provider = self._provider(geocoder, session)
        result = provider.fetch("London")

        self.assertIsNotNone(result)
        self.assertEqual(result.raw_value, 48000.0)
        self.assertIn("GBR", result.display_value)
        self.assertIn("2022", result.display_value)
        self.assertEqual(result.source, "worldbank")

        # Confirms ISO-2 -> ISO-3 conversion happened in the URL.
        called_url = session.get.call_args.args[0]
        self.assertIn("/country/GBR/", called_url)
        self.assertIn("NY.GDP.PCAP.CD", called_url)

    def test_uses_most_recent_non_null_value(self):
        # Some recent rows are null (data not yet published) — skip them.
        geocoder = _fake_geocoder(
            GeoResult(latitude=52.5, longitude=13.4, country_code="DE")
        )
        wb_resp = _response(
            _wb_payload([(None, "2024"), (None, "2023"), (52000.0, "2022"), (50000.0, "2021")])
        )
        session = MagicMock()
        session.get.return_value = wb_resp

        result = self._provider(geocoder, session).fetch("Berlin")
        self.assertEqual(result.raw_value, 52000.0)
        self.assertIn("2022", result.display_value)

    def test_returns_none_when_geocoding_finds_no_match(self):
        provider = self._provider(_fake_geocoder(None))
        self.assertIsNone(provider.fetch("Atlantis"))

    def test_returns_none_when_country_code_unmapped(self):
        # "ZZ" isn't in our ISO2->ISO3 map -> legitimate miss, no WB call.
        geocoder = _fake_geocoder(
            GeoResult(latitude=0.0, longitude=0.0, country_code="ZZ")
        )
        session = MagicMock()
        provider = self._provider(geocoder, session)

        self.assertIsNone(provider.fetch("Mystery Town"))
        session.get.assert_not_called()

    def test_returns_none_when_all_observations_null(self):
        geocoder = _fake_geocoder(
            GeoResult(latitude=0.0, longitude=0.0, country_code="DE")
        )
        wb_resp = _response(_wb_payload([(None, "2024"), (None, "2023")]))
        session = MagicMock()
        session.get.return_value = wb_resp

        self.assertIsNone(self._provider(geocoder, session).fetch("Somewhere"))

    def test_world_bank_http_error_propagates(self):
        geocoder = _fake_geocoder(
            GeoResult(latitude=51.5, longitude=-0.1, country_code="GB")
        )
        session = MagicMock()
        session.get.return_value = _response({}, status=503)

        provider = self._provider(geocoder, session)
        with self.assertRaises(requests.HTTPError):
            provider.fetch("London")

    def test_network_error_propagates(self):
        geocoder = _fake_geocoder(
            GeoResult(latitude=51.5, longitude=-0.1, country_code="GB")
        )
        session = MagicMock()
        session.get.side_effect = requests.ConnectionError("boom")

        provider = self._provider(geocoder, session)
        with self.assertRaises(requests.ConnectionError):
            provider.fetch("London")

    def test_malformed_payload_shape_raises(self):
        geocoder = _fake_geocoder(
            GeoResult(latitude=51.5, longitude=-0.1, country_code="GB")
        )
        # World Bank should return [meta, rows] — single-element response is invalid.
        session = MagicMock()
        session.get.return_value = _response([{"some": "metadata"}])

        provider = self._provider(geocoder, session)
        with self.assertRaises(ValueError):
            provider.fetch("London")

    def test_url_template_uses_provided_indicator(self):
        # Sanity check: constructor-supplied indicator flows into URL.
        url = WORLD_BANK_URL_TEMPLATE.format(iso3="DEU", indicator="SP.POP.TOTL")
        self.assertIn("DEU", url)
        self.assertIn("SP.POP.TOTL", url)


if __name__ == "__main__":
    unittest.main()

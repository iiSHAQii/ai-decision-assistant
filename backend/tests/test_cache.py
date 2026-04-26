import json
import tempfile
import unittest
from pathlib import Path

from backend.services.providers.base import DataPoint, DataProvider, Direction
from backend.services.providers.cache import JsonDiskCache
from backend.services.providers.cached import CachedProvider
from backend.services.providers.static_city import StaticCityProvider


class _Clock:
    """Manually-advanceable clock for TTL tests."""
    def __init__(self, now: float = 1000.0):
        self.now = now
    def __call__(self) -> float:
        return self.now


class _CountingProvider(DataProvider):
    """Counts fetch calls; returns a fixed value or None for unknown options."""
    direction: Direction = "higher_is_better"

    def __init__(self, criterion: str, values: dict[str, float | None]):
        self.criterion = criterion
        self._values = values
        self.fetch_calls = 0

    def fetch(self, option_name: str) -> DataPoint | None:
        self.fetch_calls += 1
        v = self._values.get(option_name)
        if v is None:
            return None
        return DataPoint(raw_value=v, display_value=str(v), source="counting")


class TestJsonDiskCache(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "cache.json"
        self.clock = _Clock()

    def tearDown(self):
        self._tmp.cleanup()

    def test_miss_when_key_absent(self):
        cache = JsonDiskCache(self.path, clock=self.clock)
        hit, value = cache.get("foo")
        self.assertFalse(hit)
        self.assertIsNone(value)

    def test_set_then_get_roundtrip(self):
        cache = JsonDiskCache(self.path, clock=self.clock)
        cache.set("foo", {"x": 1})
        hit, value = cache.get("foo")
        self.assertTrue(hit)
        self.assertEqual(value, {"x": 1})

    def test_cached_none_is_a_hit(self):
        # Storing None records a negative result; subsequent reads must report it as a hit.
        cache = JsonDiskCache(self.path, clock=self.clock)
        cache.set("foo", None)
        hit, value = cache.get("foo")
        self.assertTrue(hit)
        self.assertIsNone(value)

    def test_ttl_expiry(self):
        cache = JsonDiskCache(self.path, ttl_seconds=10, clock=self.clock)
        cache.set("foo", "bar")
        self.clock.now += 11
        hit, _ = cache.get("foo")
        self.assertFalse(hit)

    def test_persists_across_instances(self):
        c1 = JsonDiskCache(self.path, clock=self.clock)
        c1.set("foo", {"x": 1})
        c2 = JsonDiskCache(self.path, clock=self.clock)
        hit, value = c2.get("foo")
        self.assertTrue(hit)
        self.assertEqual(value, {"x": 1})

    def test_corrupt_file_falls_back_to_empty(self):
        self.path.write_text("not json", encoding="utf-8")
        cache = JsonDiskCache(self.path, clock=self.clock)
        hit, _ = cache.get("foo")
        self.assertFalse(hit)
        # Should still be writable.
        cache.set("foo", "bar")
        hit, value = cache.get("foo")
        self.assertTrue(hit)
        self.assertEqual(value, "bar")


class TestCachedProvider(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "cache.json"
        self.clock = _Clock()

    def tearDown(self):
        self._tmp.cleanup()

    def test_second_fetch_does_not_call_inner(self):
        inner = _CountingProvider("salary", {"London": 100000.0})
        cache = JsonDiskCache(self.path, clock=self.clock)
        wrapped = CachedProvider(inner, cache)

        first = wrapped.fetch("London")
        second = wrapped.fetch("London")
        self.assertEqual(first, second)
        self.assertEqual(inner.fetch_calls, 1)

    def test_cached_miss_does_not_call_inner(self):
        inner = _CountingProvider("salary", {})  # no data for any option
        cache = JsonDiskCache(self.path, clock=self.clock)
        wrapped = CachedProvider(inner, cache)

        self.assertIsNone(wrapped.fetch("Atlantis"))
        self.assertIsNone(wrapped.fetch("Atlantis"))
        self.assertEqual(inner.fetch_calls, 1)

    def test_ttl_expiry_triggers_refetch(self):
        inner = _CountingProvider("salary", {"London": 100000.0})
        cache = JsonDiskCache(self.path, ttl_seconds=10, clock=self.clock)
        wrapped = CachedProvider(inner, cache)

        wrapped.fetch("London")
        self.clock.now += 11
        wrapped.fetch("London")
        self.assertEqual(inner.fetch_calls, 2)

    def test_preserves_criterion_and_direction_from_inner(self):
        inner = _CountingProvider("salary", {})
        cache = JsonDiskCache(self.path, clock=self.clock)
        wrapped = CachedProvider(inner, cache)
        self.assertEqual(wrapped.criterion, inner.criterion)
        self.assertEqual(wrapped.direction, inner.direction)

    def test_no_op_against_static_city_provider(self):
        # Wrapping a deterministic provider should produce identical results.
        inner = StaticCityProvider("salary", raw_key="raw_salary")
        cache = JsonDiskCache(self.path, clock=self.clock)
        wrapped = CachedProvider(inner, cache)

        for city in ("London", "Berlin", "Atlantis"):
            self.assertEqual(wrapped.fetch(city), inner.fetch(city))

    def test_persists_to_disk(self):
        inner = _CountingProvider("salary", {"London": 100000.0})
        cache = JsonDiskCache(self.path, clock=self.clock)
        CachedProvider(inner, cache).fetch("London")

        # Cache file exists and contains the criterion-scoped key.
        self.assertTrue(self.path.exists())
        on_disk = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertIn("salary::London", on_disk)


if __name__ == "__main__":
    unittest.main()

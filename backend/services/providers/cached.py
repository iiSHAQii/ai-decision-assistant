from dataclasses import asdict

from backend.services.providers.base import DataPoint, DataProvider
from backend.services.providers.cache import JsonDiskCache


class CachedProvider(DataProvider):
    """Wraps a DataProvider, caching fetch results to disk per option.

    Cached negative results (None) are preserved so a missing option doesn't
    re-hit the inner provider on every request.
    """

    def __init__(self, inner: DataProvider, cache: JsonDiskCache):
        self._inner = inner
        self._cache = cache
        self.criterion = inner.criterion
        self.direction = inner.direction

    def _key(self, option_name: str) -> str:
        return f"{self.criterion}::{option_name}"

    def fetch(self, option_name: str) -> DataPoint | None:
        hit, value = self._cache.get(self._key(option_name))
        if hit:
            return DataPoint(**value) if value is not None else None

        result = self._inner.fetch(option_name)
        self._cache.set(
            self._key(option_name),
            asdict(result) if result is not None else None,
        )
        return result

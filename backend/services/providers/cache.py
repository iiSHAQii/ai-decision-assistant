import json
import time
from pathlib import Path
from threading import Lock
from typing import Any, Callable

DEFAULT_TTL_SECONDS = 7 * 24 * 3600  # one week


class JsonDiskCache:
    """File-backed key/value cache with TTL.

    Distinguishes three states for a key:
      - not cached: get(key) returns (False, None)
      - cached miss: get(key) returns (True, None)   (a previously-stored negative result)
      - cached value: get(key) returns (True, value)

    Storing None records a negative result so we don't keep re-querying a
    provider for an option it has no data for.
    """

    def __init__(
        self,
        path: Path | str,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
        clock: Callable[[], float] = time.time,
    ):
        self.path = Path(path)
        self.ttl = ttl_seconds
        self._clock = clock
        self._lock = Lock()
        self._data: dict[str, dict] = self._load()

    def _load(self) -> dict[str, dict]:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(self._data, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)

    def get(self, key: str) -> tuple[bool, Any]:
        with self._lock:
            entry = self._data.get(key)
        if entry is None:
            return (False, None)
        if self._clock() - entry.get("t", 0) > self.ttl:
            return (False, None)
        return (True, entry.get("v"))

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = {"v": value, "t": self._clock()}
            self._save()

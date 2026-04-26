from pathlib import Path

from backend.services.providers.base import DataPoint, DataProvider, Direction
from backend.services.providers.cache import JsonDiskCache
from backend.services.providers.cached import CachedProvider
from backend.services.providers.open_meteo import OpenMeteoWeatherProvider
from backend.services.providers.registry import ProviderRegistry
from backend.services.providers.static_city import StaticCityProvider

DEFAULT_CACHE_DIR = Path(".cache/providers")


def build_default_registry(cache_dir: Path | None = DEFAULT_CACHE_DIR) -> ProviderRegistry:
    """Registry pre-loaded with the default set of providers.

    Network-backed providers are wrapped in CachedProvider when cache_dir is
    given (default). Pass cache_dir=None to disable caching (useful for tests).
    """
    registry = ProviderRegistry()
    registry.register(StaticCityProvider("salary", raw_key="raw_salary"))
    registry.register(StaticCityProvider("career_opportunities"))
    registry.register(StaticCityProvider("cost_of_living"))

    weather: DataProvider = OpenMeteoWeatherProvider()
    if cache_dir is not None:
        weather = CachedProvider(
            weather, JsonDiskCache(cache_dir / "open_meteo.json")
        )
    registry.register(weather, aliases=("climate", "weather_quality"))

    return registry


__all__ = [
    "CachedProvider",
    "DataPoint",
    "DataProvider",
    "Direction",
    "JsonDiskCache",
    "OpenMeteoWeatherProvider",
    "ProviderRegistry",
    "StaticCityProvider",
    "build_default_registry",
]

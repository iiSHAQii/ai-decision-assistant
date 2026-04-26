from pathlib import Path

from backend.services.providers.base import DataPoint, DataProvider, Direction
from backend.services.providers.cache import JsonDiskCache
from backend.services.providers.cached import CachedProvider
from backend.services.providers.geocoding import GeoResult, OpenMeteoGeocoder
from backend.services.providers.open_meteo import OpenMeteoWeatherProvider
from backend.services.providers.registry import ProviderRegistry
from backend.services.providers.static_city import StaticCityProvider
from backend.services.providers.world_bank import WorldBankProvider

DEFAULT_CACHE_DIR = Path(".cache/providers")


def _wrap_with_cache(
    provider: DataProvider, cache_dir: Path | None, filename: str
) -> DataProvider:
    if cache_dir is None:
        return provider
    return CachedProvider(provider, JsonDiskCache(cache_dir / filename))


def build_default_registry(cache_dir: Path | None = DEFAULT_CACHE_DIR) -> ProviderRegistry:
    """Registry pre-loaded with the default set of providers.

    Network-backed providers are wrapped in CachedProvider when cache_dir is
    given (default). Pass cache_dir=None to disable caching (useful for tests).
    """
    registry = ProviderRegistry()

    # Salary is now country-level GDP per capita (current USD) from World Bank.
    salary = WorldBankProvider(
        criterion="salary",
        indicator="NY.GDP.PCAP.CD",
        direction="higher_is_better",
        unit="USD/yr",
    )
    registry.register(
        _wrap_with_cache(salary, cache_dir, "world_bank_salary.json"),
        aliases=("income", "wages", "average_salary"),
    )

    # Career opportunities and cost-of-living remain static utility scores
    # for now — see #16 follow-ups for replacing these with real data sources.
    # Aliases catch common LLM variants so a near-miss criterion name still routes.
    registry.register(
        StaticCityProvider("career_opportunities"),
        aliases=(
            "career_options",
            "career_growth",
            "careers",
            "job_opportunities",
            "job_market",
            "professional_opportunities",
        ),
    )
    registry.register(
        StaticCityProvider("cost_of_living"),
        aliases=("expenses", "living_cost", "living_costs", "cost"),
    )

    weather = _wrap_with_cache(
        OpenMeteoWeatherProvider(), cache_dir, "open_meteo.json"
    )
    registry.register(weather, aliases=("climate", "weather_quality"))

    return registry


__all__ = [
    "CachedProvider",
    "DataPoint",
    "DataProvider",
    "Direction",
    "GeoResult",
    "JsonDiskCache",
    "OpenMeteoGeocoder",
    "OpenMeteoWeatherProvider",
    "ProviderRegistry",
    "StaticCityProvider",
    "WorldBankProvider",
    "build_default_registry",
]

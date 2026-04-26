from backend.services.providers.base import DataPoint, DataProvider, Direction
from backend.services.providers.registry import ProviderRegistry
from backend.services.providers.static_city import StaticCityProvider


def build_default_registry() -> ProviderRegistry:
    """Registry pre-loaded with the static city dataset providers."""
    registry = ProviderRegistry()
    registry.register(StaticCityProvider("salary", raw_key="raw_salary"))
    registry.register(StaticCityProvider("career_opportunities"))
    registry.register(StaticCityProvider("cost_of_living"))
    return registry


__all__ = [
    "DataPoint",
    "DataProvider",
    "Direction",
    "ProviderRegistry",
    "StaticCityProvider",
    "build_default_registry",
]

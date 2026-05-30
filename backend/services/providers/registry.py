from backend.services.providers.base import DataProvider


class ProviderRegistry:
    """Maps criterion names (with alias support) to data providers."""

    def __init__(self):
        self._providers: dict[str, DataProvider] = {}
        self._aliases: dict[str, str] = {}

    def register(
        self,
        provider: DataProvider,
        *,
        aliases: tuple[str, ...] = (),
    ) -> None:
        self._providers[provider.criterion] = provider
        for alias in aliases:
            self._aliases[alias] = provider.criterion

    def get(self, criterion_name: str) -> DataProvider | None:
        canonical = self._aliases.get(criterion_name, criterion_name)
        return self._providers.get(canonical)

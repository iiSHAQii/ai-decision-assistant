from backend.services.providers.base import DataPoint, DataProvider, Direction

CITY_DATA: dict[str, dict] = {
    "London": {
        "salary": 0.7,
        "raw_salary": "200000$ (annual)",
        "career_opportunities": 0.8,
        "cost_of_living": 0.3,
    },
    "Berlin": {
        "salary": 0.55,
        "raw_salary": "70,000$ (annual)",
        "career_opportunities": 0.7,
        "cost_of_living": 0.3,
    },
    "Amsterdam": {
        "salary": 0.6,
        "raw_salary": "100,000$ (annual)",
        "career_opportunities": 0.75,
        "cost_of_living": 0.8,
    },
    "New York": {
        "salary": 0.9,
        "raw_salary": "250,000$ (annual)",
        "career_opportunities": 0.85,
        "cost_of_living": 0.2,
    },
}


class StaticCityProvider(DataProvider):
    """Serves pre-curated utility scores from a hardcoded dataset.

    Values in CITY_DATA are utility scores in [0, 1] (higher = better),
    so direction is "already_normalized" — values pass through unchanged.

    Lookup is case-insensitive: the LLM may emit "london" or "LONDON" while
    the dataset keys use Title Case. We normalize on read.
    """

    direction: Direction = "already_normalized"

    # Case-insensitive index built once per class — keys lowercased.
    _INDEX: dict[str, dict] = {k.lower(): v for k, v in CITY_DATA.items()}

    def __init__(self, criterion: str, raw_key: str | None = None):
        self.criterion = criterion
        self._raw_key = raw_key

    def fetch(self, option_name: str) -> DataPoint | None:
        city = self._INDEX.get(option_name.lower())
        if city is None or self.criterion not in city:
            return None
        display = city.get(self._raw_key) if self._raw_key else None
        return DataPoint(
            raw_value=city[self.criterion],
            display_value=display,
            source="static_city",
        )

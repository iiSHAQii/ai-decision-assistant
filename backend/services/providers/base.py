from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

Direction = Literal["higher_is_better", "lower_is_better", "already_normalized"]


@dataclass
class DataPoint:
    raw_value: float | None
    display_value: str | None
    source: str


class DataProvider(ABC):
    """Serves one criterion (e.g. salary) for any option (e.g. a city).

    Subclasses must set `criterion` and `direction` and implement `fetch`.
    """

    criterion: str = ""
    direction: Direction = "higher_is_better"

    @abstractmethod
    def fetch(self, option_name: str) -> DataPoint | None:
        """Return raw data for option_name, or None if unavailable."""

import unittest

from backend.decision import Criterion, Option, ParsedDecision
from backend.services.criteria_data_service import get_option_data
from backend.services.providers import ProviderRegistry
from backend.services.providers.base import DataPoint, DataProvider, Direction


def _decision(option_names, criterion_names):
    return ParsedDecision(
        question="test",
        criteria=[
            Criterion(name=c, weight=1.0 / len(criterion_names))
            for c in criterion_names
        ],
        options=[Option(name=n) for n in option_names],
    )


class TestStaticCityBehaviorPreservation(unittest.TestCase):
    """Verifies the registry refactor preserves the prior 4-city flow."""

    def test_known_cities_pass_utility_values_through(self):
        decision = _decision(
            ["London", "Berlin"],
            ["salary", "career_opportunities", "cost_of_living"],
        )
        result = get_option_data(decision)
        london = next(o for o in result.options if o.name == "London")
        berlin = next(o for o in result.options if o.name == "Berlin")
        self.assertEqual(london.criterion_values["salary"], 0.7)
        self.assertEqual(london.criterion_values["career_opportunities"], 0.8)
        self.assertEqual(london.criterion_values["cost_of_living"], 0.3)
        self.assertEqual(berlin.criterion_values["salary"], 0.55)

    def test_raw_companion_values_are_preserved(self):
        decision = _decision(["London"], ["salary"])
        result = get_option_data(decision)
        london = result.options[0]
        self.assertEqual(london.criterion_values["raw_salary"], "200000$ (annual)")

    def test_unknown_city_yields_none_values(self):
        decision = _decision(["Atlantis"], ["salary", "career_opportunities"])
        result = get_option_data(decision)
        atlantis = result.options[0]
        self.assertIsNone(atlantis.criterion_values["salary"])
        self.assertIsNone(atlantis.criterion_values["career_opportunities"])

    def test_unknown_criterion_yields_none(self):
        # Pass an explicit empty registry so this test doesn't depend on what
        # the default registry happens to contain.
        decision = _decision(["London"], ["happiness"])
        result = get_option_data(decision, registry=ProviderRegistry())
        london = result.options[0]
        self.assertIsNone(london.criterion_values["happiness"])


class _FakeRawProvider(DataProvider):
    """Provider that returns raw values requiring normalization."""

    direction: Direction = "higher_is_better"

    def __init__(self, criterion: str, values: dict[str, float | None]):
        self.criterion = criterion
        self._values = values

    def fetch(self, option_name):
        if option_name not in self._values:
            return None
        v = self._values[option_name]
        if v is None:
            return None
        return DataPoint(raw_value=v, display_value=f"{v}", source="fake")


class TestRegistryDrivenNormalization(unittest.TestCase):
    """Confirms a non-passthrough provider gets min-max normalized across options."""

    def test_higher_is_better_provider_normalizes_across_options(self):
        registry = ProviderRegistry()
        registry.register(
            _FakeRawProvider("salary", {"A": 50000.0, "B": 100000.0, "C": 200000.0})
        )
        decision = _decision(["A", "B", "C"], ["salary"])
        result = get_option_data(decision, registry=registry)
        a, b, c = result.options
        self.assertEqual(a.criterion_values["salary"], 0.0)
        self.assertAlmostEqual(b.criterion_values["salary"], 1 / 3)
        self.assertEqual(c.criterion_values["salary"], 1.0)
        # Display value flows through.
        self.assertEqual(a.criterion_values["raw_salary"], "50000.0")

    def test_alias_routing(self):
        registry = ProviderRegistry()
        registry.register(
            _FakeRawProvider("cost_of_living", {"A": 50.0, "B": 80.0}),
            aliases=("living_cost", "expenses"),
        )
        # Decision uses an alias name, not the canonical one.
        decision = _decision(["A", "B"], ["expenses"])
        result = get_option_data(decision, registry=registry)
        # The alias resolved -> values came from the cost_of_living provider.
        # Direction defaults to higher_is_better in our fake -> A:0, B:1.
        self.assertEqual(result.options[0].criterion_values["expenses"], 0.0)
        self.assertEqual(result.options[1].criterion_values["expenses"], 1.0)


if __name__ == "__main__":
    unittest.main()

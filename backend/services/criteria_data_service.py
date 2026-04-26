from backend.decision import ParsedDecision
from backend.services.normalization import min_max_normalize
from backend.services.providers import ProviderRegistry, build_default_registry

_default_registry: ProviderRegistry | None = None


def _get_default_registry() -> ProviderRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = build_default_registry()
    return _default_registry


def get_option_data(
    decision: ParsedDecision,
    registry: ProviderRegistry | None = None,
) -> ParsedDecision:
    """Enrich each option with per-criterion values from the registry.

    For each criterion in `decision.criteria`:
      - Look up a provider via the registry.
      - If absent, set the criterion value to None for every option.
      - Otherwise fetch a DataPoint per option, normalize raw values across
        the option set per the provider's direction, and write the normalized
        value into option.criterion_values[criterion]. If the provider returns
        a display_value, also store it under "raw_<criterion>".

    Returns the same decision (mutated in-place).
    """
    registry = registry or _get_default_registry()

    for option in decision.options:
        if option.criterion_values is None:
            option.criterion_values = {}

    for criterion in decision.criteria:
        provider = registry.get(criterion.name)
        if provider is None:
            for option in decision.options:
                option.criterion_values[criterion.name] = None
            continue

        points = [provider.fetch(o.name) for o in decision.options]
        normalized = min_max_normalize(
            [p.raw_value if p else None for p in points],
            provider.direction,
        )

        for option, point, norm in zip(decision.options, points, normalized):
            option.criterion_values[criterion.name] = norm
            if point and point.display_value is not None:
                option.criterion_values[f"raw_{criterion.name}"] = point.display_value

    return decision


if __name__ == "__main__":
    from backend.decision import Criterion, Option, ParsedDecision as PD

    decision = PD(
        question="Where should I move?",
        criteria=[
            Criterion(name="salary", weight=0.4),
            Criterion(name="career_opportunities", weight=0.4),
            Criterion(name="cost_of_living", weight=0.2),
        ],
        options=[Option(name="London"), Option(name="Berlin"), Option(name="Amsterdam")],
    )
    print("enriched decision:", get_option_data(decision))

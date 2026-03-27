from backend.decision import ParsedDecision


CITY_DATA = {
    "London": {
        "salary": 0.7,
        "raw_salary": 100000,
        "career_opportunities": 0.8,
        "cost_of_living": 0.3,
    },
    "Berlin": {
        "salary": 0.55,
        "raw_salary": 100000,
        "career_opportunities": 0.7,
        "cost_of_living": 0.3,
    },
    "Amsterdam": {
        "salary": 0.6,
        "raw_salary": 100000,
        "career_opportunities": 0.75,
        "cost_of_living": 0.8,
    },
    "New York": {
        "salary": 70000,
        "career_opportunities": 8.5,
        "cost_of_living": 0.2,
    },
}


def get_option_data(decision: ParsedDecision) -> ParsedDecision:
    """
    Retrieve option data for the given decision.
    Does not assign or use weights; it simply returns
    the underlying criterion values for each option.

    All *normalized* values are expected to be in the
    range [0, 1]. For some criteria (e.g. ``salary``)
    we also return a corresponding ``raw_<name>`` value
    if it exists in ``CITY_DATA`` (e.g. ``raw_salary``).
    The score is expected to be a utility score, e.g "cost of 0.1" 
    indicates that a citiy is very expensive.

    This function mutates the given ParsedDecision in-place by
    enriching each Option with a ``criterion_values`` mapping:

        option.criterion_values = {
            "salary": 0.7,
            "raw_salary": 100000,
            "cost_of_living": 0.9,
            ...
        }

    and then returns the same ParsedDecision instance.
    """
    option_names = [o.name for o in decision.options]
    criterion_names = [c.name for c in decision.criteria]

    # Enrich each Option in the decision with its per-criterion values
    name_to_option = {o.name: o for o in decision.options}

    for option_name in option_names:
        option = name_to_option.get(option_name)
        if option is None:
            continue

        option_data = CITY_DATA.get(option_name, {})
        criterion_values: dict[str, float | None] = {}

        if option_data:
            for criterion in criterion_names:
                # Normalized value (if present)
                criterion_values[criterion] = option_data.get(criterion)

                # Raw companion value, e.g. "raw_salary"
                raw_key = f"raw_{criterion}"
                if raw_key in option_data:
                    criterion_values[raw_key] = option_data[raw_key]
        else:
            criterion_values = {criterion: None for criterion in criterion_names}

        option.criterion_values = criterion_values

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
        options=[
            Option(name="London"),
            Option(name="Berlin"),
            Option(name="Amsterdam"),
        ],
    )

    enriched = get_option_data(decision)
    print("enriched decision:", enriched)

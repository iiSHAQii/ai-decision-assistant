from backend.decision import ParsedDecision


CITY_DATA = {
    "London": {
        "salary": 0.7,
        "raw_salary": 100000,
        "career_opportunities": 0.8,
        "cost_of_living": 0.9,
    },
    "Berlin": {
        "salary": 0.55,
        "raw_salary": 100000,
        "career_opportunities": 0.7,
        "cost_of_living": 6,
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
        "cost_of_living": 9.5,
    },
}


def get_option_data(decision: ParsedDecision) -> dict:
    """
    Retrieve option data for the given decision.
    Does not assign or use weights; it simply returns
    the underlying criterion values for each option.

    All *normalized* values are expected to be in the
    range [0, 1]. For some criteria (e.g. ``salary``)
    we also return a corresponding ``raw_<name>`` value
    if it exists in ``CITY_DATA`` (e.g. ``raw_salary``).

    Output format (example):
    {
        "London": {
            "salary": 0.1,
            "raw_salary": 100000,
            "cost_of_living": 0.3,
        },
        "Berlin": {
            "salary": 0.2,
            "raw_salary": 100000,
            "cost_of_living": 0.4,
        }
    }
    """
    result: dict[str, dict[str, float | None]] = {}

    option_names = [o.name for o in decision.options]
    criterion_names = [c.name for c in decision.criteria]

    for option_name in option_names:
        option_data = CITY_DATA.get(option_name, {})
        result[option_name] = {}

        if option_data:
            for criterion in criterion_names:
                # Normalized value (if present)
                result[option_name][criterion] = option_data.get(criterion)

                # Raw companion value, e.g. "raw_salary"
                raw_key = f"raw_{criterion}"
                if raw_key in option_data:
                    result[option_name][raw_key] = option_data[raw_key]
        else:
            result[option_name] = {criterion: None for criterion in criterion_names}

    return result


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

    data = get_option_data(decision)
    print("data:", data)

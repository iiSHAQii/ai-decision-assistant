from backend.decision import ParsedDecision


CITY_DATA = {
    "London": {
        "salary": 65000,
        "career_opportunities": 8,
        "cost_of_living": 9,
    },
    "Berlin": {
        "salary": 55000,
        "career_opportunities": 7,
        "cost_of_living": 6,
    },
    "Amsterdam": {
        "salary": 60000,
        "career_opportunities": 7.5,
        "cost_of_living": 8,
    },
}


def get_option_data(decision: ParsedDecision) -> dict:
    """
    Retrieve option data for the given decision.
    Does not assign or use weights; it simply returns
    the underlying criterion values for each option.

    Output format (example):
    {
        "London": {
            "salary": 65000,
            "cost_of_living": 9,
        },
        "Berlin": {
            "salary": 55000,
            "cost_of_living": 6,
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
                result[option_name][criterion] = option_data.get(criterion)
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
    print(data)

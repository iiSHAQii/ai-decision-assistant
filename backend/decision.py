import pprint

from pydantic import BaseModel, confloat


class Criterion(BaseModel):
    name: str
    weight: confloat(ge=0.0, le=1.0)
    # will be filled later
    total_score: float | None = None


class Option(BaseModel):
    name: str
    score: float | None = None
    # Per-criterion values for this option (e.g. salary, cost_of_living, raw_salary, ...)
    criterion_values: dict[str, float | None] | None = None


class ParsedDecision(BaseModel):
    question: str
    criteria: list[Criterion]
    options: list[Option]

    # Will later be filled by the LLM
    explanation: str | None = None
    recommended_option: str | None = None


if __name__ == "__main__":
    json_str = """
    {
        "question": "Should I move to London or Berlin? Salary and career opportunities are important to me.",
        "criteria": [
            {"name": "Salary", "weight": 0.4},
            {"name": "Career Opportunities", "weight": 0.4},
            {"name": "Cost of Living", "weight": 0.2}
        ],
        # options and option scores are not required
        "options": [{"name": "London", "score": 7.5}, {"name": "Berlin", "score": 6.2}]
    }
    """
    parsed_decision = ParsedDecision.model_validate_json(json_str)
    pprint.pprint(parsed_decision)


def rank_options(decision: ParsedDecision) -> ParsedDecision:
    """
    Computes weighted scores for options and ranks them.

    Assumes that criterion_values in each Option are already scaled appropriately
    by get_option_data for direct use in weighted sum calculation.

    Args:
        decision: The ParsedDecision object containing options and criteria.

    Returns:
        The ParsedDecision object with options ranked by score.
    """
    for option in decision.options:
        option.score = 0.0
        if option.criterion_values:
            for criterion in decision.criteria:
                criterion_value = option.criterion_values.get(criterion.name)
                if criterion_value is not None:
                    # Directly use the criterion value (assumed to be scaled)
                    # and multiply by the criterion weight.
                    option.score += criterion.weight * criterion_value
                # If criterion_value is None, it contributes 0 to the score for this criterion.

    # Sort options by score descending
    # Use a large negative number for None scores to place them at the end
    decision.options.sort(
        key=lambda option: option.score if option.score is not None else -float("inf"),
        reverse=True,
    )

    # Set recommended option based on the top-ranked option
    if decision.options and decision.options[0].score is not None:
        decision.recommended_option = decision.options[0].name
    else:
        # Handle cases where no options could be scored or ranked
        decision.recommended_option = None

    return decision

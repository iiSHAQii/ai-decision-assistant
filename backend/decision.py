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

    # Criteria that had no data for any option — dropped from scoring and
    # surfaced to the user so they can interpret the result honestly.
    skipped_criteria: list[str] | None = None


if __name__ == "__main__":
    json_str = """
    {
        "question": "Should I move to London or Berlin? Salary and career opportunities are important to me.",
        "criteria": [
            {"name": "Salary", "weight": 0.4},
            {"name": "Career Opportunities", "weight": 0.4},
            {"name": "Cost of Living", "weight": 0.2}
        ],
        "options": [{"name": "London", "score": 7.5}, {"name": "Berlin", "score": 6.2}]
    }
    """
    parsed_decision = ParsedDecision.model_validate_json(json_str)
    pprint.pprint(parsed_decision)


def rank_options(decision: ParsedDecision) -> ParsedDecision:
    """Compute weighted-average scores per option, drop fully-missing criteria,
    and pick a recommendation only when the top option strictly beats the rest.

    For each option, score = sum(weight * value) / sum(weight) over criteria
    where the option has a non-None value — a true weighted average in [0, 1].
    Missing values do not contribute to either numerator or denominator, so an
    option isn't penalized for our data gaps.

    Criteria with no data for ANY option are dropped entirely and recorded in
    `decision.skipped_criteria` so the UI can disclose the gap to the user.

    `recommended_option` is set to the top-ranked option only when it has a
    real score AND that score strictly exceeds the runner-up's. Otherwise None
    — to avoid implying confidence we don't have.
    """
    # Identify criteria with at least one non-None value across all options.
    skipped: list[str] = []
    active_criteria: list[Criterion] = []
    for criterion in decision.criteria:
        has_any_data = any(
            opt.criterion_values is not None
            and opt.criterion_values.get(criterion.name) is not None
            for opt in decision.options
        )
        if has_any_data:
            active_criteria.append(criterion)
        else:
            skipped.append(criterion.name)
    decision.skipped_criteria = skipped

    # Compute each option's weighted average over active criteria with data.
    for option in decision.options:
        if not option.criterion_values:
            option.score = None
            continue
        weighted_sum = 0.0
        weight_sum = 0.0
        for criterion in active_criteria:
            value = option.criterion_values.get(criterion.name)
            if value is None:
                continue
            weighted_sum += criterion.weight * value
            weight_sum += criterion.weight
        option.score = (weighted_sum / weight_sum) if weight_sum > 0 else None

    # Sort: real scores first (descending), None scores last.
    decision.options.sort(key=lambda o: (o.score is None, -(o.score or 0.0)))

    # Recommendation: only when top option strictly beats #2 (or stands alone).
    decision.recommended_option = _pick_recommendation(decision.options)

    return decision


def _pick_recommendation(options: list[Option]) -> str | None:
    if not options or options[0].score is None:
        return None
    if len(options) == 1:
        return options[0].name
    runner_up = options[1].score
    if runner_up is None or options[0].score > runner_up:
        return options[0].name
    return None  # tied at the top — no honest single recommendation

from pydantic import BaseModel, confloat
import pprint


class Criterion(BaseModel):
    name: str
    weight: confloat(ge=0.0, le=1.0)
    # will be filled later
    total_score: float | None = None


class Option(BaseModel):
    name: str
    score: float | None = None


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

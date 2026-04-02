import json
import os

from dotenv import load_dotenv
from google import genai

from backend.decision import Criterion, Option, ParsedDecision

load_dotenv(override=True)


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

FALLBACK_EXPLANATION = (
    "We could not generate a detailed explanation right now, but the ranked "
    "decision results are available above."
)


def _strip_markdown_fences(text: str) -> str:
    """Normalize model output by removing markdown code fences when present."""
    normalized = (text or "").strip()
    if normalized.startswith("```"):
        normalized = normalized.split("```")[1]
        if normalized.startswith("json"):
            normalized = normalized[4:]
    return normalized.strip()


def _build_prompt(question: str) -> str:
    return f"""
You are a decision analysis assistant.
Given a decision question, extract the following and return ONLY valid JSON, no explanation, no markdown:
- options: list of options being compared
- criteria: list of evaluation criteria
- weights: dictionary of criteria to decimal weights that sum to 1.0

Important rules:
- Use lowercase snake_case names for criteria.
- Examples:
    salary
    cost_of_living
    career_opportunities
    safety
    weather
- The criteria list and the weight keys must match exactly.
- Do NOT invent or add generic criteria (e.g. "other_factors", "misc", "other", "other_factor").
  Only include criteria that are explicitly mentioned by the user, or clearly implied by the question.
- The number of criteria can be 1 or more.
  - If the question mentions only ONE criterion, return exactly ONE criterion and set its weight to 1.0.

Decision question: "{question}"

Return this exact structure:
{{
  "options": ["Option1", "Option2"],
  "criteria": ["Criterion1", "Criterion2"],
  "weights": {{
    "Criterion1": 0.5,
    "Criterion2": 0.5
  }}
}}
"""


def parse_decision_raw(question: str) -> dict:
    """Call the LLM and return the raw JSON payload as a dict."""
    prompt = _build_prompt(question)
    response = client.models.generate_content(
        model="models/gemini-2.5-flash", contents=prompt
    )
    text = _strip_markdown_fences(response.text or "")
    return json.loads(text)


def _build_explanation_prompt(decision: ParsedDecision) -> str:
    """Build the prompt for explanation generation from enriched ParsedDecision data."""
    payload = {
        "question": decision.question,
        "criteria": [
            {
                "name": c.name,
                "weight": c.weight,
                "total_score": c.total_score,
            }
            for c in decision.criteria
        ],
        "options": [
            {
                "name": o.name,
                "score": o.score,
                "criterion_values": o.criterion_values,
            }
            for o in decision.options
        ],
        "recommended_option": decision.recommended_option,
    }

    return f"""
You are a decision analysis assistant.
Using the decision payload below, generate a concise, human-readable explanation of the result.

Rules:
- Return plain text only (no markdown or bullet points).
- Keep it concise: 2 to 3 sentences, maximum 70 words.
- Mention only the most important criteria, key ranking driver, and one major trade-off.
- Reference the recommended option if available.
- If some values are missing, acknowledge uncertainty in one short clause.

Decision payload:
{json.dumps(payload, ensure_ascii=True)}
"""


def generate_explanation(decision: ParsedDecision) -> str:
    """Generate explanation text from ParsedDecision data using the LLM."""
    prompt = _build_explanation_prompt(decision)
    response = client.models.generate_content(
        model="models/gemini-2.5-flash", contents=prompt
    )
    explanation = _strip_markdown_fences(response.text or "")
    if not explanation:
        raise ValueError("LLM returned an empty explanation")
    return explanation


def decision_from_payload(payload: dict, question: str) -> ParsedDecision:
    """Adapt the raw LLM payload into a ParsedDecision domain object."""
    options = [Option(name=o) for o in payload.get("options", [])]

    weights = payload.get("weights", {}) or {}
    criteria = [
        Criterion(name=c, weight=weights.get(c, 0.0))
        for c in payload.get("criteria", [])
    ]

    return ParsedDecision(
        question=question,
        criteria=criteria,
        options=options,
    )


def parse_decision(question: str) -> ParsedDecision:
    """Public API: get a ParsedDecision for a question."""
    payload = parse_decision_raw(question)
    return decision_from_payload(payload, question)


"""
Test the end-point:
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/decisions/analyze" -Method POST -ContentType "application/json" -Body '{"question": "Should I move to London or Berlin? Salary and career matters most."}'
"""

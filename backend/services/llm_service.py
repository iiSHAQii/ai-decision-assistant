import json
import os

from dotenv import load_dotenv
from google import genai

from backend.decision import Criterion, Option, ParsedDecision

load_dotenv(override=True)


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text.strip())


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

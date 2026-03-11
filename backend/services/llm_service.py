import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def parse_decision(question: str) -> dict:
    prompt = f"""
You are a decision analysis assistant.
Given a decision question, extract the following and return ONLY valid JSON, no explanation, no markdown:
- options: list of options being compared
- criteria: list of evaluation criteria
- weights: dictionary of criteria to decimal weights that sum to 1.0

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
    response = client.models.generate_content(
        model="models/gemini-2.5-flash", contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


"""
Test the end-point:
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/decisions/analyze" -Method POST -ContentType "application/json" -Body '{"question": "Should I move to London or Berlin? Salary and career matters most."}'
"""

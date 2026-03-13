from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.decision import ParsedDecision
from backend.services.criterion_data_service import get_option_data
from backend.services.llm_service import parse_decision

app = FastAPI()


class AnalyzeRequest(BaseModel):
    question: str


@app.post("/api/decisions/analyze", response_model=ParsedDecision)
async def analyze_decision(request: AnalyzeRequest):
    try:
        result = parse_decision(request.question)
        option_data = get_option_data(
            result
        )  # next step: score the options and enrich the result with the scores
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

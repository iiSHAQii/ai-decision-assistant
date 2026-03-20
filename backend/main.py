from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.decision import ParsedDecision, rank_options
from backend.services.criteria_data_service import get_option_data
from backend.services.llm_service import parse_decision

app = FastAPI()


class AnalyzeRequest(BaseModel):
    question: str


@app.post("/api/decisions/analyze", response_model=ParsedDecision)
async def analyze_decision(request: AnalyzeRequest):
    try:
        result = parse_decision(request.question)
        result = get_option_data(result)
        # next step: score the options and enrich the result with the scores
        ranked_result = rank_options(result)
        print(ranked_result)
        return ranked_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

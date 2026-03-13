from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.decision import ParsedDecision
from backend.services.llm_service import parse_decision

app = FastAPI()


class AnalyzeRequest(BaseModel):
    question: str


@app.post("/api/decisions/analyze", response_model=ParsedDecision)
async def analyze_decision(request: AnalyzeRequest):
    try:
        result = parse_decision(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

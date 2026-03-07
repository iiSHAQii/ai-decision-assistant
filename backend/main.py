from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnalyzeRequest(BaseModel):
    decision_question: str

class AnalyzeResponse(BaseModel):
    message: str
    decision_question: str

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_decision(request: AnalyzeRequest):
    """
    Analyzes a decision question and provides a dummy response.
    """
    return AnalyzeResponse(
        message=f"Received your decision question: '{request.decision_question}'",
        decision_question=request.decision_question
    )

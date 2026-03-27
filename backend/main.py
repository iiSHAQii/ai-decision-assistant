from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.decision import ParsedDecision, rank_options
from backend.services.criteria_data_service import get_option_data
from backend.services.llm_service import parse_decision

app = FastAPI()

# Allow the Vite dev server (and localhost variants) to call the API during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

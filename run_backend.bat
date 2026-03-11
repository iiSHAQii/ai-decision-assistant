@echo off
echo Starting FastAPI backend...
call venv\Scripts\activate
uvicorn backend.main:app --reload
pause

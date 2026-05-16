@echo off

echo ================================
echo Starting FastAPI Backend...
echo ================================

start cmd /k "cd backend && ..\venv\Scripts\activate && python -m uvicorn main:app --reload"

timeout /t 3 >nul

echo ================================
echo Starting Vue Frontend...
echo ================================

start cmd /k "cd frontend && npm run dev"

echo ================================
echo Application Started
echo ================================

pause
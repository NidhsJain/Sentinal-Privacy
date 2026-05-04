@echo off
echo ===================================================
echo     Sentinel Privacy - Startup Script
echo ===================================================

echo.
echo [1/2] Starting Sentinel Privacy Backend (FastAPI + Ollama)...
start "Backend Server" cmd /k "call .venv\Scripts\activate.bat && cd SGP_6THSEM_CHATBOT\SGP_6THSEM_CHATBOT && python rag_file.py"

echo.
echo [2/2] Starting Sentinel Privacy Frontend (Streamlit)...
start "Frontend Dashboard" cmd /k "call .venv\Scripts\activate.bat && streamlit run app.py"

echo.
echo Both services are now starting in separate windows!
echo You can close this window.
pause

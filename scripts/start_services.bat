@echo off
echo ========================================
echo Starting PulseAI Services
echo ========================================
echo.

echo Starting Model API on port 8000...
start "Model API" cmd /k "python -m MLOps_Engineer3.api.serve"

timeout /t 3 /nobreak > nul

echo Starting Dashboard on port 8501...
start "Dashboard" cmd /k "streamlit run MLOps_Engineer4\app\main.py"

echo.
echo ========================================
echo Services Started!
echo ========================================
echo API: http://localhost:8000
echo Dashboard: http://localhost:8501
echo.
echo Press any key to exit (services will keep running)...
pause > nul

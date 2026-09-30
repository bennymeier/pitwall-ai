@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\streamlit.exe" (
    echo Bitte zuerst install.bat ausfuehren.
    pause
    exit /b 1
)

.venv\Scripts\streamlit.exe run app.py

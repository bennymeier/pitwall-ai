@echo off
setlocal
cd /d "%~dp0"

echo Erstelle virtuelle Umgebung...
if not exist ".venv\Scripts\python.exe" py -3.12 scripts\create_venv.py .venv
if errorlevel 1 (
    echo Fehler: Python 3.12 wurde nicht gefunden.
    pause
    exit /b 1
)

echo Pruefe pip...
.venv\Scripts\python.exe -m pip --version >nul 2>&1
if errorlevel 1 (
    .venv\Scripts\python.exe -m ensurepip --upgrade --default-pip
    if errorlevel 1 (
        echo Fehler: pip konnte nicht eingerichtet werden.
        pause
        exit /b 1
    )
)

echo Installiere Abhaengigkeiten...
.venv\Scripts\python.exe -m pip install -e ".[dev]"
if errorlevel 1 (
    echo Fehler bei der Installation.
    pause
    exit /b 1
)

echo Installation erfolgreich.
pause

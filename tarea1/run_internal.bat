@echo off
REM ============================================
REM Lanzador de la aplicación Python (Windows)
REM ============================================

REM Cambia al directorio donde está este .bat
cd /d "%~dp0"

REM Comprobamos si python está disponible
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

REM Ejecutamos la aplicacion
python html2graphml.py

REM Mantener la ventana abierta al terminar
pause

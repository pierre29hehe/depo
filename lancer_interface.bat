@echo off
REM Script de lancement de l'interface graphique (Windows)

echo 🚀 Lancement de l'interface graphique...
echo.

python financial_analyzer_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Erreur lors du lancement
    pause
)

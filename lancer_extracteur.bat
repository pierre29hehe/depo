@echo off
REM Script de lancement de l'extracteur de tableaux PDF (Windows)

echo.
echo ========================================
echo  Extracteur de Tableaux PDF
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo Verification des dependances...
pip install pdfplumber pandas openpyxl >nul 2>&1

REM Lancer le programme
echo.
echo Lancement de l'interface...
python pdf_table_extractor.py

pause

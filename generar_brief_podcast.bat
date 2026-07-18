@echo off
setlocal

echo ==========================================
echo Brief podcast Comercio Digital - Generacion
echo ==========================================

set "PROJECT_DIR=%~dp0"
set "PYTHON_EXE=%LOCALAPPDATA%\PythonVenvs\comercio-digital\Scripts\python.exe"
set "LOG_DIR=%PROJECT_DIR%logs"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set LOG_FILE=%LOG_DIR%\brief_podcast.log

echo. >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"
echo Inicio brief podcast: %date% %time% >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"

cd /d "%PROJECT_DIR%"

"%PYTHON_EXE%" generar_brief_newsletter.py --periodicidad quincenal --max 6 >> "%LOG_FILE%" 2>&1

echo Fin brief podcast: %date% %time% >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"

echo Brief de podcast generado.
echo Revisa outputs\podcast antes de usarlo como base de guion.
REM pause

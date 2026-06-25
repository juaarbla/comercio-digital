@echo off
setlocal

echo ==========================================
echo Newsletter Comercio Digital - Generacion
echo ==========================================

set PROJECT_DIR=C:\Users\Juan\Google Drive\00_CDI_press
set PYTHON_EXE=C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\Scripts\python.exe
set LOG_DIR=%PROJECT_DIR%\logs

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set LOG_FILE=%LOG_DIR%\newsletter_quincenal.log

echo. >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"
echo Inicio newsletter: %date% %time% >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"

cd /d "%PROJECT_DIR%"

"%PYTHON_EXE%" generar_newsletter.py --periodicidad quincenal --force >> "%LOG_FILE%" 2>&1

echo Fin newsletter: %date% %time% >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"

echo Newsletter generada.
echo Revisa docs\newsletter antes de publicar.
REM pause
@echo off
setlocal

echo ==========================================
echo Newsletter Comercio Digital - Mailgun
echo ==========================================

set PROJECT_DIR=C:\Users\Juan\Google Drive\00_CDI_press
set PYTHON_EXE=C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\Scripts\python.exe
set LOG_DIR=%PROJECT_DIR%\logs

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set LOG_FILE=%LOG_DIR%\newsletter_mailgun_bat.log

echo. >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"
echo Inicio Mailgun: %date% %time% >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"

cd /d "%PROJECT_DIR%"

"%PYTHON_EXE%" enviar_newsletter_mailgun.py %* >> "%LOG_FILE%" 2>&1

echo Fin Mailgun: %date% %time% >> "%LOG_FILE%"
echo ========================================== >> "%LOG_FILE%"

echo Proceso Mailgun finalizado.
echo Revisa logs\newsletter_mailgun.log y logs\newsletter_mailgun_bat.log.
REM pause

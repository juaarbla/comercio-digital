@echo off
chcp 65001 >nul
setlocal EnableExtensions

set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "PROJECT_DIR=C:\Users\Juan\Google Drive\00_CDI_press"
set "VENV_PY=%LOCALAPPDATA%\PythonVenvs\comercio-digital\Scripts\python.exe"
set "LOG_DIR=%PROJECT_DIR%\logs"
set "LOG_FILE=%LOG_DIR%\publicacion_diaria.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo.
echo Comercio Digital - publicacion diaria
echo Log: %LOG_FILE%
echo.

echo.>> "%LOG_FILE%"
echo ============================================================>> "%LOG_FILE%"
echo Inicio publicacion diaria: %DATE% %TIME%>> "%LOG_FILE%"
echo ============================================================>> "%LOG_FILE%"

cd /d "%PROJECT_DIR%"
if errorlevel 1 (
  echo ERROR: No se pudo entrar en PROJECT_DIR
  echo ERROR: No se pudo entrar en PROJECT_DIR>> "%LOG_FILE%"
  exit /b 1
)

if not exist "%VENV_PY%" (
  echo ERROR: No se encuentra el Python del entorno virtual
  echo ERROR: No se encuentra el Python del entorno virtual>> "%LOG_FILE%"
  echo Ruta: %VENV_PY%>> "%LOG_FILE%"
  exit /b 1
)

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo ERROR: No parece un repositorio Git
  echo ERROR: No parece un repositorio Git>> "%LOG_FILE%"
  exit /b 1
)

echo Ejecutando git pull...
echo Ejecutando git pull...>> "%LOG_FILE%"
git pull --ff-only >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
  echo ERROR: git pull fallo. No se continua.
  echo ERROR: git pull fallo. No se continua.>> "%LOG_FILE%"
  exit /b 1
)

echo Ejecutando pipeline...
echo Ejecutando pipeline...>> "%LOG_FILE%"
"%VENV_PY%" run_pipeline.py >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
  echo ERROR: run_pipeline.py fallo. No se publica.
  echo ERROR: run_pipeline.py fallo. No se publica.>> "%LOG_FILE%"
  echo Revisa el log: %LOG_FILE%
  exit /b 1
)

echo Preparando cambios de docs...
echo Preparando cambios de docs...>> "%LOG_FILE%"
git add docs/ >> "%LOG_FILE%" 2>&1

git diff --cached --quiet
if not errorlevel 1 (
  echo No hay cambios en docs. No se crea commit.
  echo No hay cambios en docs. No se crea commit.>> "%LOG_FILE%"
  echo Fin sin cambios: %DATE% %TIME%>> "%LOG_FILE%"
  exit /b 0
)

echo Creando commit automatico...
echo Creando commit automatico...>> "%LOG_FILE%"
git commit -m "Actualiza web diaria" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
  echo ERROR: git commit fallo.
  echo ERROR: git commit fallo.>> "%LOG_FILE%"
  echo Revisa el log: %LOG_FILE%
  exit /b 1
)

echo Subiendo a GitHub...
echo Subiendo a GitHub...>> "%LOG_FILE%"
git push >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
  echo ERROR: git push fallo.
  echo ERROR: git push fallo.>> "%LOG_FILE%"
  echo Revisa el log: %LOG_FILE%
  exit /b 1
)

echo Publicacion completada correctamente.
echo Publicacion completada correctamente: %DATE% %TIME%>> "%LOG_FILE%"
exit /b 0

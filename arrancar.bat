@echo off
chcp 65001 >nul
title Comercio Digital - Panel de control

cd /d "%~dp0"

rem El entorno virtual se guarda fuera de Google Drive.
rem LOCALAPPDATA cambia automaticamente segun el usuario y el equipo.
set "VENV_DIR=%LOCALAPPDATA%\PythonVenvs\comercio-digital"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creando entorno virtual por primera vez en:
    echo %VENV_DIR%
    echo.
    py -m venv "%VENV_DIR%"

    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        echo Comprueba que Python y el lanzador py estan instalados.
        pause
        exit /b 1
    )

    call "%VENV_DIR%\Scripts\activate.bat"

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias.
        pause
        exit /b 1
    )

    echo Entorno virtual creado correctamente.
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
)

if not exist ".env" (
    echo AVISO: No se encontro el archivo .env
    echo Copia env.example como .env y rellena los valores necesarios.
    pause
    exit /b 1
)

:MENU
cls
echo.
echo  =============================================
echo    Comercio Digital - comerciodigital.net
echo  =============================================
echo.
echo    1. Proceso completo
echo    2. Proceso completo + publicar en GitHub
echo    3. Solo leer feeds
echo    4. Solo clasificar
echo    5. Solo enriquecimiento docente
echo    6. Solo imagenes
echo    7. Solo generar web
echo    8. Solo publicar ^(git push^)
echo    9. Abrir web local
echo    0. Salir
echo.
set /p OPCION="   Elige una opcion: "

if "%OPCION%"=="1" goto COMPLETO
if "%OPCION%"=="2" goto COMPLETO_GIT
if "%OPCION%"=="3" goto FEEDS
if "%OPCION%"=="4" goto CLASIFICAR
if "%OPCION%"=="5" goto ENRIQUECER
if "%OPCION%"=="6" goto IMAGENES
if "%OPCION%"=="7" goto WEB
if "%OPCION%"=="8" goto GIT
if "%OPCION%"=="9" goto ABRIR
if "%OPCION%"=="0" goto FIN
goto MENU

:FEEDS
echo.
echo  Leyendo feeds y resumiendo...
echo  -----------------------------------------------
python news_aggregator.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:CLASIFICAR
echo.
echo  Clasificando por RA y CE...
echo  -----------------------------------------------
python clasificador_ra.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:ENRIQUECER
echo.
echo  Generando preguntas, conceptos y actividades...
echo  -----------------------------------------------
python enriquecer_docente.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:IMAGENES
echo.
echo  Buscando imagenes destacadas...
echo  -----------------------------------------------
python imagen_destacada.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:WEB
echo.
echo  Generando web...
echo  -----------------------------------------------
python generar_web.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:GIT
echo.
echo  Publicando en GitHub Pages...
echo  -----------------------------------------------
call :PUBLICAR_GITHUB
goto PAUSA

:ABRIR
start "" "docs\index.html"
goto MENU

:COMPLETO
echo.
echo  Proceso completo...
echo  -----------------------------------------------
python run_pipeline.py

if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Listo. Revisa docs\index.html antes de publicar.
goto PAUSA

:COMPLETO_GIT
echo.
echo  Proceso completo + publicacion...
echo  -----------------------------------------------
python run_pipeline.py

if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Publicando en GitHub Pages...
call :PUBLICAR_GITHUB

if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Publicado. En unos minutos estara disponible en GitHub Pages.
goto PAUSA

:PUBLICAR_GITHUB
git pull --rebase --autostash origin main

if errorlevel 1 (
    echo.
    echo  ERROR: no se pudo sincronizar con origin/main.
    exit /b 1
)

git add docs/

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Actualizacion web %date% %time%"
) else (
    echo.
    echo  No hay cambios nuevos en docs para confirmar.
)

git push origin main

if errorlevel 1 (
    echo.
    echo  ERROR: fallo al subir cambios a GitHub.
    exit /b 1
)

exit /b 0

:ERROR_PROCESO
echo.
echo  =============================================
echo  ERROR: el proceso no se ha completado.
echo  Revisa los mensajes anteriores.
echo  =============================================
goto PAUSA

:PAUSA
echo.
echo  -----------------------------------------------
echo  Pulsa cualquier tecla para volver al menu...
pause >nul
goto MENU

:FIN
echo.
echo  Hasta luego.
echo.

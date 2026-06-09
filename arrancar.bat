@echo off
chcp 65001 >nul
title Comercio Digital - Panel de control

cd /d "%~dp0"

if not exist "venv\" (
    echo Creando entorno virtual por primera vez...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo Listo.
)

call venv\Scripts\activate.bat
pip install feedparser anthropic python-dotenv requests -q >nul 2>&1

if not exist ".env" (
    echo AVISO: No se encontro .env
    echo Copia .env.example y rellena los valores.
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
echo    5. Solo imagenes
echo    6. Solo generar web
echo    7. Solo publicar (git push)
echo    8. Abrir web local
echo    0. Salir
echo.
set /p OPCION="   Elige una opcion: "

if "%OPCION%"=="1" goto COMPLETO
if "%OPCION%"=="2" goto COMPLETO_GIT
if "%OPCION%"=="3" goto FEEDS
if "%OPCION%"=="4" goto CLASIFICAR
if "%OPCION%"=="5" goto IMAGENES
if "%OPCION%"=="6" goto WEB
if "%OPCION%"=="7" goto GIT
if "%OPCION%"=="8" goto ABRIR
if "%OPCION%"=="0" goto FIN
goto MENU

:FEEDS
echo.
echo  Leyendo feeds y resumiendo...
echo  -----------------------------------------------
python news_aggregator.py
goto PAUSA

:CLASIFICAR
echo.
echo  Clasificando por RA y CE...
echo  -----------------------------------------------
python clasificador_ra.py
goto PAUSA

:IMAGENES
echo.
echo  Buscando imagenes destacadas...
echo  -----------------------------------------------
python imagen_destacada.py
goto PAUSA

:WEB
echo.
echo  Generando web...
echo  -----------------------------------------------
python generar_web.py
goto PAUSA

:GIT
echo.
echo  Publicando en GitHub Pages...
echo  -----------------------------------------------
call :PUBLICAR_GITHUB
goto PAUSA

:ABRIR
start docs\index.html
goto MENU

:COMPLETO
echo.
echo  Proceso completo...
echo  -----------------------------------------------
python news_aggregator.py
echo.
python clasificador_ra.py
echo.
python imagen_destacada.py
echo.
python generar_web.py
echo.
echo  Listo. Revisa docs\index.html antes de publicar.
goto PAUSA

:COMPLETO_GIT
echo.
echo  Proceso completo + publicacion...
echo  -----------------------------------------------
python news_aggregator.py
echo.
python clasificador_ra.py
echo.
python imagen_destacada.py
echo.
python generar_web.py
echo.
echo  Publicando en GitHub Pages...
call :PUBLICAR_GITHUB
echo.
echo  Publicado. En 1-2 min disponible en GitHub Pages.
goto PAUSA

:PUBLICAR_GITHUB
git pull --rebase --autostash origin main
if errorlevel 1 (
    echo.
    echo  ERROR: no se pudo sincronizar con origin/main.
    exit /b 1
)

git add docs/
git commit -m "Actualizacion %date% %time%" >nul 2>&1
git push origin main
if errorlevel 1 (
    echo.
    echo  ERROR: fallo al subir cambios a GitHub.
    exit /b 1
)
exit /b 0

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

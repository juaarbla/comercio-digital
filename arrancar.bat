@echo off
chcp 65001 >nul
title Comercio Digital - Panel de control

cd /d "%~dp0"

rem ==========================================================
rem Comercio Digital - Panel de control
rem Proyecto: https://comerciodigital.net
rem ==========================================================

rem El entorno virtual se guarda fuera de Google Drive.
rem LOCALAPPDATA cambia automaticamente segun el usuario y el equipo.
set "VENV_DIR=%LOCALAPPDATA%\PythonVenvs\comercio-digital"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo.
    echo Creando entorno virtual por primera vez en:
    echo %VENV_DIR%
    echo.
    py -m venv "%VENV_DIR%"

    if errorlevel 1 (
        echo.
        echo ERROR: No se pudo crear el entorno virtual.
        echo Comprueba que Python y el lanzador py estan instalados.
        pause
        exit /b 1
    )

    call "%VENV_DIR%\Scripts\activate.bat"

    echo.
    echo Instalando dependencias...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

    if errorlevel 1 (
        echo.
        echo ERROR: No se pudieron instalar las dependencias.
        pause
        exit /b 1
    )

    echo.
    echo Entorno virtual creado correctamente.
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
)

if not exist ".env" (
    echo.
    echo AVISO: No se encontro el archivo .env
    echo Copia .env.example como .env y rellena los valores necesarios.
    echo.
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
echo    2. Proceso completo + publicar SOLO web docs/
echo    3. Proceso completo + publicar TODO el proyecto
echo.
echo    4. Solo leer feeds
echo    5. Solo clasificar
echo    6. Solo enriquecimiento docente
echo    7. Solo imagenes
echo    8. Solo generar web principal
echo    9. Solo generar aula
echo   10. Solo SEO tecnico
echo.
echo   11. Abrir portada local
echo   12. Abrir aula local
echo   13. Estado de Git
echo.
echo   14. Publicar SOLO web docs/
echo   15. Publicar TODO el proyecto
echo.
echo    0. Salir
echo.
set /p OPCION="   Elige una opcion: "

if "%OPCION%"=="1" goto COMPLETO
if "%OPCION%"=="2" goto COMPLETO_GIT_DOCS
if "%OPCION%"=="3" goto COMPLETO_GIT_PROYECTO
if "%OPCION%"=="4" goto FEEDS
if "%OPCION%"=="5" goto CLASIFICAR
if "%OPCION%"=="6" goto ENRIQUECER
if "%OPCION%"=="7" goto IMAGENES
if "%OPCION%"=="8" goto WEB
if "%OPCION%"=="9" goto AULA
if "%OPCION%"=="10" goto SEO
if "%OPCION%"=="11" goto ABRIR_PORTADA
if "%OPCION%"=="12" goto ABRIR_AULA
if "%OPCION%"=="13" goto ESTADO_GIT
if "%OPCION%"=="14" goto GIT_DOCS
if "%OPCION%"=="15" goto GIT_PROYECTO
if "%OPCION%"=="0" goto FIN
goto MENU

:FEEDS
echo.
echo  Leyendo feeds y resumiendo noticias...
echo  -----------------------------------------------
python news_aggregator.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:CLASIFICAR
echo.
echo  Clasificando por modulo, RA y CE...
echo  -----------------------------------------------
python clasificador_ra.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:ENRIQUECER
echo.
echo  Generando capa docente...
echo  -----------------------------------------------
python enriquecer_docente.py --forzar
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
echo  Generando web principal...
echo  -----------------------------------------------
python generar_web.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:AULA
echo.
echo  Generando pagina de aula...
echo  -----------------------------------------------
python generar_aula.py --max-noticias 25
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:SEO
echo.
echo  Ejecutando SEO tecnico...
echo  -----------------------------------------------
python generar_seo.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:ABRIR_PORTADA
if exist "docs\index.html" (
    start "" "docs\index.html"
) else (
    echo.
    echo No existe docs\index.html. Ejecuta primero el proceso completo.
)
goto PAUSA

:ABRIR_AULA
if exist "docs\aula.html" (
    start "" "docs\aula.html"
) else (
    echo.
    echo No existe docs\aula.html. Ejecuta primero generar aula o proceso completo.
)
goto PAUSA

:ESTADO_GIT
echo.
echo  Estado de Git...
echo  -----------------------------------------------
git status
goto PAUSA

:GIT_DOCS
echo.
echo  Publicando SOLO la web docs/ en GitHub...
echo  -----------------------------------------------
call :PUBLICAR_DOCS
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:GIT_PROYECTO
echo.
echo  Publicando TODO el proyecto en GitHub...
echo  -----------------------------------------------
call :PUBLICAR_PROYECTO
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:COMPLETO
echo.
echo  Ejecutando proceso completo...
echo  -----------------------------------------------
python run_pipeline.py
if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Proceso completo finalizado.
echo  Revisa docs\index.html y docs\aula.html antes de publicar.
goto PAUSA

:COMPLETO_GIT_DOCS
echo.
echo  Ejecutando proceso completo...
echo  -----------------------------------------------
python run_pipeline.py
if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Publicando SOLO docs/...
call :PUBLICAR_DOCS
if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Web publicada. Revisa:
echo  https://comerciodigital.net
echo  https://comerciodigital.net/aula.html
goto PAUSA

:COMPLETO_GIT_PROYECTO
echo.
echo  Ejecutando proceso completo...
echo  -----------------------------------------------
python run_pipeline.py
if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Publicando TODO el proyecto...
call :PUBLICAR_PROYECTO
if errorlevel 1 goto ERROR_PROCESO

echo.
echo  Proyecto publicado. Revisa GitHub y GitHub Pages.
goto PAUSA

:PUBLICAR_DOCS
git pull --rebase --autostash origin main

if errorlevel 1 (
    echo.
    echo ERROR: no se pudo sincronizar con origin/main.
    exit /b 1
)

git add docs/

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Actualiza web %date% %time%"
) else (
    echo.
    echo No hay cambios nuevos en docs/ para confirmar.
)

git push origin main

if errorlevel 1 (
    echo.
    echo ERROR: fallo al subir cambios a GitHub.
    exit /b 1
)

exit /b 0

:PUBLICAR_PROYECTO
git pull --rebase --autostash origin main

if errorlevel 1 (
    echo.
    echo ERROR: no se pudo sincronizar con origin/main.
    exit /b 1
)

git add docs/
git add *.py
git add *.md
git add arrancar.bat
git add .gitignore
git add .env.example

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Actualiza proyecto %date% %time%"
) else (
    echo.
    echo No hay cambios nuevos para confirmar.
)

git push origin main

if errorlevel 1 (
    echo.
    echo ERROR: fallo al subir cambios a GitHub.
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

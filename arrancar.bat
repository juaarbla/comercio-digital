@echo off
chcp 65001 >nul
title Comercio Digital - Panel de control

cd /d "%~dp0"

set "VENV_DIR=%LOCALAPPDATA%\PythonVenvs\comercio-digital"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo.
    echo Creando entorno virtual en:
    echo %VENV_DIR%
    py -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    call "%VENV_DIR%\Scripts\activate.bat"
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
)

if not exist ".env" (
    echo.
    echo AVISO: No se encontro el archivo .env
    echo Copia .env.example como .env y rellena los valores necesarios.
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
echo    7. Solo enriquecer conceptos curriculares
echo    8. Solo imagenes
echo    9. Solo generar web principal
echo   10. Solo generar fichas de aula
echo   11. Solo generar aula
echo   12. Solo SEO tecnico
echo   13. Generar newsletter semanal
echo   14. Generar newsletter quincenal
echo.
echo   15. Abrir portada local
echo   16. Abrir aula local
echo   17. Abrir newsletter local
echo   18. Estado de Git
echo.
echo   19. Publicar SOLO web docs/
echo   20. Publicar TODO el proyecto
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
if "%OPCION%"=="7" goto CONCEPTOS
if "%OPCION%"=="8" goto IMAGENES
if "%OPCION%"=="9" goto WEB
if "%OPCION%"=="10" goto FICHAS
if "%OPCION%"=="11" goto AULA
if "%OPCION%"=="12" goto SEO
if "%OPCION%"=="13" goto NEWSLETTER_SEMANAL
if "%OPCION%"=="14" goto NEWSLETTER_QUINCENAL
if "%OPCION%"=="15" goto ABRIR_PORTADA
if "%OPCION%"=="16" goto ABRIR_AULA
if "%OPCION%"=="17" goto ABRIR_NEWSLETTER
if "%OPCION%"=="18" goto ESTADO_GIT
if "%OPCION%"=="19" goto GIT_DOCS
if "%OPCION%"=="20" goto GIT_PROYECTO
if "%OPCION%"=="0" goto FIN
goto MENU

:FEEDS
python news_aggregator.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:CLASIFICAR
python clasificador_ra.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:ENRIQUECER
python enriquecer_docente.py --forzar
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:CONCEPTOS
python enriquecer_conceptos.py --sobrescribir
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:IMAGENES
python imagen_destacada.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:WEB
python generar_web.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:FICHAS
python generar_fichas_aula.py --max-fichas 10 --limpiar
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:AULA
python generar_aula.py --max-noticias 25
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:SEO
python generar_seo.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:NEWSLETTER_SEMANAL
python generar_newsletter.py --periodicidad semanal --force
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:NEWSLETTER_QUINCENAL
python generar_newsletter.py --periodicidad quincenal --force
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:ABRIR_PORTADA
start "" "docs\index.html"
goto PAUSA

:ABRIR_AULA
start "" "docs\aula.html"
goto PAUSA

:ABRIR_NEWSLETTER
start "" "docs\newsletter\index.html"
goto PAUSA

:ESTADO_GIT
git status
goto PAUSA

:GIT_DOCS
call :PUBLICAR_DOCS
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:GIT_PROYECTO
call :PUBLICAR_PROYECTO
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:COMPLETO
python run_pipeline.py
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:COMPLETO_GIT_DOCS
python run_pipeline.py
if errorlevel 1 goto ERROR_PROCESO
call :PUBLICAR_DOCS
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:COMPLETO_GIT_PROYECTO
python run_pipeline.py
if errorlevel 1 goto ERROR_PROCESO
call :PUBLICAR_PROYECTO
if errorlevel 1 goto ERROR_PROCESO
goto PAUSA

:PUBLICAR_DOCS
git pull --rebase --autostash origin main
if errorlevel 1 exit /b 1
git add docs/
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Actualiza web %date% %time%"
) else (
    echo No hay cambios nuevos en docs/.
)
git push origin main
if errorlevel 1 exit /b 1
exit /b 0

:PUBLICAR_PROYECTO
git pull --rebase --autostash origin main
if errorlevel 1 exit /b 1
git add docs/
git add data/curriculo/
git add *.py
git add *.md
git add arrancar.bat
git add .gitignore
git add .env.example
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Actualiza proyecto %date% %time%"
) else (
    echo No hay cambios nuevos para confirmar.
)
git push origin main
if errorlevel 1 exit /b 1
exit /b 0

:ERROR_PROCESO
echo.
echo ERROR: el proceso no se ha completado.
pause
goto MENU

:PAUSA
echo.
echo Pulsa cualquier tecla para volver al menu...
pause >nul
goto MENU

:FIN
echo Hasta luego.

@echo off
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

title MCP Comercio Digital

cd /d "%~dp0"

set "PYTHON_MCP=%LOCALAPPDATA%\PythonVenvs\comercio-digital\Scripts\python.exe"
set "MCP_SERVER=mcp_servers\comercio_digital\server.py"

echo ============================================
echo MCP Comercio Digital
echo ============================================
echo.
echo Proyecto:
echo %cd%
echo.
echo Python:
echo %PYTHON_MCP%
echo.
echo Servidor:
echo %MCP_SERVER%
echo.

if not exist "%PYTHON_MCP%" (
    echo ERROR: No se encuentra el Python del entorno virtual:
    echo %PYTHON_MCP%
    echo.
    echo Revisa que exista:
    echo %%LOCALAPPDATA%%\PythonVenvs\comercio-digital\Scripts\python.exe
    pause
    exit /b 1
)

if not exist "%MCP_SERVER%" (
    echo ERROR: No se encuentra el servidor MCP:
    echo %MCP_SERVER%
    pause
    exit /b 1
)

echo Iniciando servidor MCP...
echo Para detenerlo: CTRL + C
echo.

"%PYTHON_MCP%" "%MCP_SERVER%"

echo.
echo Servidor MCP detenido.
pause
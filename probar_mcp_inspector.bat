@echo off
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

title Probar MCP Comercio Digital con Inspector

cd /d "%~dp0"

set "VENV_DIR=%LOCALAPPDATA%\PythonVenvs\comercio-digital"
set "PYTHON_MCP=%VENV_DIR%\Scripts\python.exe"
set "MCP_CLI=%VENV_DIR%\Scripts\mcp.exe"
set "MCP_SERVER=mcp_servers\comercio_digital\server.py"

echo ============================================
echo MCP Comercio Digital - Inspector
echo ============================================
echo.
echo Proyecto:
echo %cd%
echo.
echo Python recomendado:
echo %PYTHON_MCP%
echo.
echo MCP CLI:
echo %MCP_CLI%
echo.
echo Servidor:
echo %MCP_SERVER%
echo.

if not exist "%PYTHON_MCP%" (
    echo ERROR: No se encuentra el Python del entorno virtual:
    echo %PYTHON_MCP%
    pause
    exit /b 1
)

if not exist "%MCP_SERVER%" (
    echo ERROR: No se encuentra el servidor MCP:
    echo %MCP_SERVER%
    pause
    exit /b 1
)

if not exist "%MCP_CLI%" (
    echo No se encuentra mcp.exe en el entorno.
    echo Instalando requisitos del MCP...
    echo.
    "%PYTHON_MCP%" -m pip install -r mcp_servers\comercio_digital\requirements.txt
)

if not exist "%MCP_CLI%" (
    echo ERROR: Sigue sin encontrarse mcp.exe:
    echo %MCP_CLI%
    echo.
    echo Prueba manual:
    echo "%PYTHON_MCP%" -m pip install "mcp[cli]"
    pause
    exit /b 1
)

echo Abriendo MCP Inspector...
echo.
echo Si el Inspector intenta usar uv y falla, configura manualmente:
echo.
echo Transport Type:
echo STDIO
echo.
echo Command:
echo %PYTHON_MCP%
echo.
echo Arguments:
echo "%cd:\=/%/mcp_servers/comercio_digital/server.py"
echo.

"%MCP_CLI%" dev "%MCP_SERVER%"

pause
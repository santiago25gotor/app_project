@echo off
cd /d "%~dp0"
title Sistema de Gestion de Futbol

echo ==========================================
echo   Iniciando Sistema de Gestion de Futbol
echo ==========================================
echo.

:: 1. Detectar Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :found_python
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :found_python
)

echo [ERROR] No se encontro Python.
echo Por favor instala Python desde https://www.python.org/downloads/
echo O desde la Microsoft Store.
echo.
pause
exit /b

:found_python
echo [INFO] Usando Python: %PYTHON_CMD%
echo.

:: 2. Instalar dependencias
echo [INFO] Verificando dependencias...
%PYTHON_CMD% -m pip install fastapi uvicorn pydantic python-multipart pandas requests matplotlib
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Fallo la instalacion de dependencias.
    echo Verifica tu conexion a internet.
    echo.
    pause
    exit /b
)

:: 3. Variables de entorno para envio de correo
echo.
echo [INFO] Configurando correo de verificacion...
set EMAIL_USER=gotoramados@gmail.com
set EMAIL_PASS=ljnmmmfgboinxglb

:: 4. Iniciar Servidor
echo.
echo [INFO] Iniciando servidor...
echo Si el navegador no se abre, visita: http://localhost:8000
echo Presiona CTRL+C para detener.
echo.
%PYTHON_CMD% server.py
pause

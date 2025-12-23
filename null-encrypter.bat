@echo off
REM null-Encrypter CLI para Windows
REM Wrapper que ejecuta el script Python

setlocal

REM Verificar si Python está instalado
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python no esta instalado
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Ejecutar el script portable
python "%~dp0null-encrypter-portable.py" %*

endlocal

@echo off
setlocal EnableDelayedExpansion

echo ===================================================
echo   Compilador ROBUSTO de null-Encrypter UI
echo ===================================================
echo.

REM 1. Verificar Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no encontrado.
    pause
    exit /b 1
)

REM 2. Crear entorno virtual limpio para evitar conflictos
echo [1/5] Creando entorno virtual (venv)...
if exist "build_venv" (
    echo       Eliminando entorno anterior...
    rmdir /s /q "build_venv"
)
python -m venv build_venv

REM 3. Activar entorno e instalar dependencias
echo [2/5] Activando entorno e instalando dependencias...
call build_venv\Scripts\activate.bat

echo       Actualizando pip...
python -m pip install --upgrade pip --quiet

echo       Instalando Kivy y dependencias de Windows...
REM Instalamos dependencias especificas de Windows para Kivy
python -m pip install "kivy[base]" kivy_deps.sdl2 kivy_deps.glew plyer pyinstaller

REM 4. Verificar instalacion
echo [3/5] Verificando instalacion de Kivy...
python -c "import kivy; print('   Kivy version:', kivy.__version__)"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Kivy no se pudo importar correctamente.
    pause
    exit /b 1
)

REM 5. Compilar
echo.
echo [4/5] Compilando ejecutable...
echo       Usando hooks de Kivy para PyInstaller...

REM Usamos python -m PyInstaller para asegurar que usa el del venv
python -m PyInstaller --onefile ^
    --name null-encrypter-ui ^
    --noconsole ^
    --hidden-import kivy ^
    --hidden-import plyer ^
    --hidden-import kivy_deps.sdl2 ^
    --hidden-import kivy_deps.glew ^
    main.py

REM 6. Limpieza y Resultado
echo.
if exist "dist\null-encrypter-ui.exe" (
    echo [5/5] EXITO! Ejecutable creado en:
    echo       %CD%\dist\null-encrypter-ui.exe
    echo.
    echo       IMPORTANTE: Si al ejecutarlo falla, intenta ejecutarlo desde la terminal
    echo       para ver los errores.
) else (
    echo [ERROR] No se genero el archivo .exe
)

REM Desactivar venv
deactivate
pause

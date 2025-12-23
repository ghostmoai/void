"""
This module handles the compilation of the EncryptorX application and its installer
using PyInstaller.
"""
# © 2025 ghostmoai. Todos los derechos reservados.
import subprocess
import os
import sys
import shutil
from pathlib import Path

# Directorio base del script, para que funcione sin importar desde dónde se ejecute
SCRIPT_DIR = Path(__file__).parent.resolve()

# =========================
#  CONFIGURACIÓN DE COMPILACIÓN
# =========================
APP_NAME = "null"
APP_SCRIPT = "main.py" 
INSTALLER_SCRIPT = "installer.py"
ICON_FILE = "163290-logotipo_de_piton-piton-icono-lenguaje_de_programacion-logotipo-3840x2160.ico"  # Icono para la aplicación principal
INSTALLER_ICON_FILE = "163290-logotipo_de_piton-piton-icono-lenguaje_de_programacion-logotipo-3840x2160.ico" # Icono para el instalador
VERSION_INFO_FILE = "version_info.txt" # Archivo con copyright y versión para el .exe
LICENSE_NAME = "Licencia Pública – EncryptorX.txt"

APP_EXE_NAME = "null-encrypter-ui"
INSTALLER_EXE_NAME = "setup"

# Usar rutas absolutas para los directorios de salida y trabajo
DIST_DIR = SCRIPT_DIR / "dist"
BUILD_DIR = SCRIPT_DIR / "build"

REQUIRED_PACKAGES = [
    "kivy[base]",
    "kivy_deps.sdl2",
    "kivy_deps.glew",
    "plyer",
    "pyinstaller"
]

def check_and_install_dependencies():
    """Verifica e intenta instalar las dependencias necesarias."""
    print(f"\n>>> Entorno Python actual: {sys.executable}")
    print(">>> Verificando dependencias del sistema...")
    
    # Intentar importar kivy primero para ver si ya está visible
    try:
        import kivy
        print(f"    [INFO] Kivy detectado versión: {kivy.__version__}")
        print(f"    [INFO] Ruta de Kivy: {kivy.__path__}")
    except ImportError:
        print("    [INFO] Kivy no detectado al inicio. Se intentará instalar.")

    for package in REQUIRED_PACKAGES:
        print(f"    Verificando/Instalando {package}...")
        try:
            # Quitamos DEVNULL para ver errores si los hay
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"    [OK] {package} procesado.")
        except subprocess.CalledProcessError as e:
            print(f"    [ERROR] Falló la instalación de {package}. Código: {e.returncode}")
            
    # Verificar nuevamente después de instalar
    try:
        import kivy
        print("    [OK] Kivy es importable ahora.")
    except ImportError:
        print("    [CRITICO] Kivy sigue sin poder importarse después de la instalación.")
        print("    Esto causará que PyInstaller falle o genere un exe incompleto.")

def compile_with_pyinstaller(script_path: Path, exe_name: str, icon_file: Path, is_windowed: bool = False, use_uac: bool = False, extra_data: list = None):
    """Función genérica para compilar un script con PyInstaller."""
    print(f"\n>>> Compilando {script_path.name} en {exe_name}.exe...")

    if not script_path.is_file():
        print(f"[ERROR] El archivo de script '{script_path.name}' no se encontró en la ruta: {script_path}")
        return False
    
    command = [
        sys.executable, "-m", "PyInstaller", # Usar el módulo PyInstaller del python actual
        "--noconfirm",
        "--onefile",
        "--name", exe_name,
        # Especificar directorios de salida para evitar desorden
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
    ]

    # Imports ocultos específicos para Kivy y Plyer
    hidden_imports = [
        "kivy",
        "plyer",
        "kivy_deps.sdl2",
        "kivy_deps.glew"
    ]
    for imp in hidden_imports:
        command.extend(["--hidden-import", imp])
    
    if is_windowed:
        command.append("--noconsole") # Preferible a --windowed para consistencia
    
    if use_uac:
        command.append("--uac-admin")
        
    # Añadir información de versión y copyright desde el archivo
    version_file_path = SCRIPT_DIR / VERSION_INFO_FILE
    if version_file_path.is_file():
        command.extend(["--version-file", str(version_file_path)])
    else:
        print(f"    [AVISO] Archivo de versión '{VERSION_INFO_FILE}' no encontrado. No se añadirá copyright al .exe.")

    if icon_file and icon_file.is_file():
        command.extend(["--icon", str(icon_file)])
    else:
        print(f"    [AVISO] Archivo de icono '{icon_file.name}' no encontrado. Se usará el icono por defecto.")

    # Añadir datos adicionales (como otros .exe o archivos) al paquete
    if extra_data:
        for data_item in extra_data:
            command.extend(["--add-data", data_item])

    command.append(str(script_path))
    
    print(f"    Comando: {' '.join(command)}")
    
    try:
        # Usamos Popen para mostrar la salida en tiempo real
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        for line in iter(process.stdout.readline, ''):
            print(f"    {line.strip()}")
        process.wait()
        
        if process.returncode != 0:
            print(f"[ERROR] PyInstaller falló con código de error {process.returncode}.")
            return False
            
        print(f"[ÉXITO] '{exe_name}.exe' creado en la carpeta '{DIST_DIR}'.")
        return True
        
    except FileNotFoundError:
        print("[ERROR] El comando 'pyinstaller' no se encontró.")
        return False
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado durante la compilación: {e}")
        return False

def main():
    """Script principal para compilar la aplicación y el instalador."""
    print("--- Iniciando proceso de compilación para EncryptorX ---")
    
    # 0. Verificar dependencias
    check_and_install_dependencies()

    # 1. Limpiar compilaciones anteriores para empezar desde cero.
    print("\n>>> Limpiando artefactos de compilaciones anteriores...")
    try:
        if DIST_DIR.exists():
            shutil.rmtree(DIST_DIR)
            print(f"    [OK] Directorio '{DIST_DIR.name}' eliminado.")
        if BUILD_DIR.exists():
            shutil.rmtree(BUILD_DIR)
            print(f"    [OK] Directorio '{BUILD_DIR.name}' eliminado.")
    except Exception as e:
        print(f"    [ERROR] No se pudo limpiar los directorios: {e}")
        # No salimos, intentamos continuar

    # Definir rutas absolutas a los archivos de origen
    app_script_path = SCRIPT_DIR / APP_SCRIPT
    installer_script_path = SCRIPT_DIR / INSTALLER_SCRIPT
    
    # Definir rutas a los iconos
    app_icon = SCRIPT_DIR / ICON_FILE
    installer_icon = SCRIPT_DIR / INSTALLER_ICON_FILE

    # 2. Compilar la aplicación principal (main.py -> null-encrypter-ui.exe)
    if not compile_with_pyinstaller(app_script_path, APP_EXE_NAME, app_icon, is_windowed=True, use_uac=False):
        sys.exit(1)

    # 3. Definir los archivos que se empaquetarán DENTRO del instalador.
    data_to_bundle = []
    app_exe_path_in_dist = DIST_DIR / f"{APP_EXE_NAME}.exe"
    if app_exe_path_in_dist.exists():
        data_to_bundle.append(f"{app_exe_path_in_dist}{os.pathsep}.")
    else:
        print(f"[ERROR] No se encontró '{app_exe_path_in_dist}' para empaquetar en el instalador.")
        sys.exit(1)

    license_path = SCRIPT_DIR / LICENSE_NAME
    if license_path.exists():
        data_to_bundle.append(f"{license_path}{os.pathsep}.")
    else:
        print(f"[AVISO] Archivo de licencia no encontrado. No se incluirá en el instalador.")

    # 4. Compilar el instalador (installer.py -> setup.exe)
    if not compile_with_pyinstaller(installer_script_path, INSTALLER_EXE_NAME, installer_icon, is_windowed=False, use_uac=False, extra_data=data_to_bundle):
        sys.exit(1)

    # 5. Limpiar archivos temporales finales de PyInstaller
    print("\n>>> Limpiando archivos de compilación temporales...")
    if BUILD_DIR.exists(): shutil.rmtree(BUILD_DIR)
    for spec_file in SCRIPT_DIR.glob("*.spec"): spec_file.unlink()
    print("    [OK] Archivos temporales eliminados.")

    print("\n--- Proceso de compilación finalizado ---")
    print(f"Tus archivos de distribución están listos en la carpeta '{DIST_DIR}'.")
    print(f"\n- Para nuevos usuarios: Distribuye '{INSTALLER_EXE_NAME}.exe'.")
    print(f"- Para actualizaciones: Sube '{APP_EXE_NAME}.exe'.")

if __name__ == "__main__":
    main()

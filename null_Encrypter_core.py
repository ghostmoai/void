# -*- coding: utf-8 -*-
"""
EncryptorX
==========

This script provides a GUI application for encrypting and decrypting text and files.

It also includes functionality for auto-updating the application on Windows and for
uninstalling it.

This script is the main entry point for the EncryptorX application.
It handles the application's lifecycle, including updates, uninstallation,
and launching the main GUI.

Functions:
----------
- parse_version_tuple(version_str): Parses a version string into a tuple of integers.
- check_for_updates(): Checks for new versions of the application on GitHub.
- apply_update(download_url, in_gui=False): Applies an update to the application.
- get_desktop_path(): Gets the path to the user's desktop.
- remove_from_path(path_to_remove): Removes a directory from the user's PATH.
- remove_uninstaller_registry(): Removes the uninstaller registry key.
- uninstall_application(): Uninstalls the application.
- get_or_create_key(): Gets the encryption key or creates a new one.
- encrypt_text(text): Encrypts a string of text.
- decrypt_text(encrypted_text): Decrypts a string of text.
- encrypt_file(file_path): Encrypts a file.
- decrypt_file(file_path): Decrypts a file.
- run_gui_app(): Runs the main GUI application.
- attach_to_console(): Attaches the process to a console for output.
- main(): The main function of the script.

"""
import os
import sys
import subprocess
import ctypes
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
if os.name == 'nt':
    import winreg
    import win32api
else:
    winreg = None
    win32api = None
APP_VERSION = "v1.2.2"
APP_NAME = "EncryptorX"
GITHUB_API_URL = "https://api.github.com/repos/ghostmoai/encryterX_V2/releases/latest"
EXE_NAME = "EncryptorX.exe"
APP_DATA_DIR = Path(os.getenv("APPDATA") or os.path.expanduser("~/.config")) / APP_NAME
KEY_FILE = APP_DATA_DIR / "key.key"
LICENSE_NAME = "Licencia Pública – EncryptorX.txt"

INSTALL_DIR = Path(sys.executable).parent / APP_NAME if getattr(sys, 'frozen', False) else Path(__file__).parent / "dist" / APP_NAME
def parse_version_tuple(version_str):
    if not version_str:
        return None
    if version_str.startswith('v'):
        version_str = version_str[1:]
    try:
        return tuple(map(int, version_str.split('.')))
    except (ValueError, TypeError):
        return None
def check_for_updates():
    """Checks for new versions of the application on GitHub."""
    if os.name != 'nt':
        return None
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()
        release_data = response.json()
        latest_version_str = release_data.get("tag_name")
        if not latest_version_str:
            return None
        current_version_tuple = parse_version_tuple(APP_VERSION)
        latest_version_tuple = parse_version_tuple(latest_version_str)
        if current_version_tuple and latest_version_tuple and latest_version_tuple > current_version_tuple:
            assets = release_data.get("assets", [])
            for asset in assets:
                if asset.get("name") == EXE_NAME:
                    return latest_version_str, asset.get("browser_download_url")
    except Exception:
        pass
    return None
def apply_update(download_url, in_gui=False):
    """Applies an update to the application."""
    if os.name != 'nt':
        message = "La actualización automática solo está disponible en Windows."
        if in_gui: messagebox.showwarning("Funcionalidad no disponible", message)
        else: print(f"[ADVERTENCIA] {message}")
        return
    if not getattr(sys, 'frozen', False):
        message = "La actualización automática solo funciona en la versión compilada (.exe)."
        if in_gui: messagebox.showwarning("Modo Desarrollo", message)
        else: print(f"[ADVERTENCIA] {message}")
        return
    try:
        current_exe_path = Path(sys.executable)
        new_exe_path = current_exe_path.with_suffix(".new")
        update_bat_path = current_exe_path.parent / "update.bat"
        print("[*] Descargando nueva versión...")
        response = requests.get(download_url, timeout=60)
        response.raise_for_status()
        with open(new_exe_path, "wb") as f: f.write(response.content)
        print("[+] Descarga completa.")
        bat_content = f'@echo off\necho Actualizando {APP_NAME}...\ntimeout /t 2 /nobreak > nul\ndel "{current_exe_path}"\nrename "{new_exe_path}" "{current_exe_path.name}"\nstart "" "{current_exe_path}"\n(goto) 2>nul & del "%~f0"'
        with open(update_bat_path, "w") as f: f.write(bat_content)
        print("[*] Lanzando script de actualización y cerrando la aplicación...")
        subprocess.Popen(f'"{update_bat_path}"', shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        sys.exit(0)
    except Exception as e:
        error_message = f"Ocurrió un error al aplicar la actualización: {e}"
        if in_gui: messagebox.showerror("Error de Actualización", error_message)
        else: print(f"[ERROR] {error_message}", file=sys.stderr)
def get_desktop_path():
    """Gets the path to the user's desktop."""
    if os.name == 'nt':
        try:
            shell_folders_key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, shell_folders_key) as key:
                desktop_path, _ = winreg.QueryValueEx(key, "Desktop")
            return Path(os.path.expandvars(desktop_path))
        except Exception:
            return Path(os.path.expanduser("~/Desktop"))
    else:
        return Path(os.path.expanduser("~/Desktop"))
DESKTOP_DIR = get_desktop_path()
START_MENU_DIR = Path(os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs")) / APP_NAME
def remove_from_path(path_to_remove):
    if os.name != 'nt':
        return
    print(f"[*] Eliminando '{path_to_remove}' del PATH...")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as env_key:
            current_path, _ = winreg.QueryValueEx(env_key, "Path")
            new_path_parts = [p for p in current_path.split(';') if p and Path(p).resolve() != path_to_remove.resolve()]
            new_path = ';'.join(new_path_parts)
            winreg.SetValueEx(env_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001A, 0, "Environment")
            print("[+] PATH limpiado con éxito.")
    except Exception as e:
        print(f"[!] Error al limpiar el PATH: {e}")
def remove_uninstaller_registry():
    if os.name != 'nt':
        return
    print("[*] Eliminando registro del desinstalador...")
    uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{uninstall_key}\\{APP_NAME}")
        print("[+] Registro del desinstalador eliminado.")
    except FileNotFoundError:
        print("[-] No se encontró registro del desinstalador.")
    except Exception as e:
        print(f"[!] Error al eliminar el registro: {e}")
def uninstall_application():
    if os.name != 'nt':
        print("La desinstalación solo está disponible en Windows.")
        return
    print(f"\n--- Desinstalando {APP_NAME} ---")
    current_exe_path = Path(sys.executable)
    install_dir = current_exe_path.parent
    remove_from_path(install_dir)
    desktop_shortcut = DESKTOP_DIR / f"{APP_NAME}.lnk"
    if desktop_shortcut.exists():
        desktop_shortcut.unlink()
        print("[+] Acceso directo del escritorio eliminado.")
    if START_MENU_DIR.exists():
        shutil.rmtree(START_MENU_DIR)
        print("[+] Carpeta del menú de inicio eliminada.")
    remove_uninstaller_registry()
    if install_dir.exists():
        print(f"[*] Preparando la eliminación final de: {install_dir}")
        uninstall_bat_path = Path(os.environ["TEMP"]) / f"uninstall_{APP_NAME}.bat"
        bat_content = f'"""\n@echo off\necho Finalizando desinstalacion...\ntimeout /t 3 /nobreak > nul\nrmdir /s /q \"{install_dir}\"\n(goto) 2>nul & del "%~f0"\n"""'
        try:
            with open(uninstall_bat_path, "w") as f:
                f.write(bat_content)
            subprocess.Popen(f'"{uninstall_bat_path}"', shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            print("[+] La limpieza final se completará en segundo plano.")
        except Exception as e:
            print(f"[!] No se pudo crear el script de limpieza final: {e}")
            print(f"    Por favor, elimina manualmente la carpeta: {install_dir}")
    print(f"\n[ÉXITO] {APP_NAME} se ha desinstalado.")
    sys.exit(0)
def get_or_create_key():
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = os.urandom(32)
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
ENCRYPTION_KEY = get_or_create_key()
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ',':'--..--', '.':'.-.-.-', '?':'..--..', '/':'/-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-', ' ':'/' }
INV_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}
SUBST_MAP_ENCRYPT = {'1': 'A', '0': 'G', '.': 'M', '-': 'R', ' ': 'Z', '/': 'Y', '~': 'X'}
SUBST_MAP_DECRYPT = {v: k for k, v in SUBST_MAP_ENCRYPT.items()}
def encrypt_text(text):
    # This function uses two different encryption methods based on the length of the input text.
    # This is likely for obfuscation and is not a secure encryption method.

    if len(text) < 5:
        # Short text encryption: Binary representation of even characters, Morse code of odd characters,
        # then substitution cipher.
        encrypted_parts = []
        for i, char in enumerate(text):
            if i % 2 == 0:
                encrypted_parts.append(format(ord(char), '08b'))
            else:
                encrypted_parts.append(MORSE_CODE_DICT.get(char.upper(), ''))
        intermediate_text = '~'.join(encrypted_parts)
        return ''.join([SUBST_MAP_ENCRYPT.get(char, char) for char in intermediate_text])
    else:
        # Long text encryption: Caesar cipher (shift by 9), then convert to binary.
        caesar_shifted_text = ''
        for char in text:
            if 'a' <= char <= 'z':
                shifted_char = chr((ord(char) - ord('a') + 9) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                shifted_char = chr((ord(char) - ord('A') + 9) % 26 + ord('A'))
            else:
                shifted_char = char
            caesar_shifted_text += shifted_char
        return ''.join(format(ord(char), '08b') for char in caesar_shifted_text)
def decrypt_text(encrypted_text):
    is_binary = all(char in '01' for char in encrypted_text)
    if is_binary:
        # Long text decryption: Binary to Caesar cipher (shift by -9).
        try:
            binary_chunks = [encrypted_text[i:i+8] for i in range(0, len(encrypted_text), 8)]
            caesar_shifted_text = ''.join([chr(int(chunk, 2)) for chunk in binary_chunks])
            decrypted_text = ''
            for char in caesar_shifted_text:
                if 'a' <= char <= 'z':
                    shifted_char = chr((ord(char) - ord('a') - 9 + 26) % 26 + ord('a'))
                elif 'A' <= char <= 'Z':
                    shifted_char = chr((ord(char) - ord('A') - 9 + 26) % 26 + ord('A'))
                else:
                    shifted_char = char
                decrypted_text += shifted_char
            return decrypted_text
        except (ValueError, TypeError):
            raise ValueError("Texto cifrado (binario) inválido.")
    else:
        # Short text decryption: Substitution cipher to Morse/Binary to original text.
        try:
            intermediate_text = ''.join([SUBST_MAP_DECRYPT.get(char, char) for char in encrypted_text])
            encrypted_parts = intermediate_text.split('~')
            decrypted_text = ''
            for i, part in enumerate(encrypted_parts):
                if i % 2 == 0:
                    decrypted_text += chr(int(part, 2))
                else:
                    decrypted_text += INV_MORSE_CODE_DICT.get(part, '')
            return decrypted_text
        except (ValueError, TypeError, KeyError):
            raise ValueError("Texto cifrado (letras) inválido o clave incorrecta.")
def encrypt_file(file_path):
    # WARNING: This function uses a simple XOR cipher, which is not secure.
    # It should not be used for encrypting sensitive data.
    encrypted_file_path = f"{file_path}.enc"
    try:
        with open(file_path, "rb") as input_file, open(encrypted_file_path, "wb") as output_file:
            buffer = input_file.read(4096)
            key_index = 0
            while buffer:
                encrypted_buffer = bytearray()
                for byte in buffer:
                    encrypted_buffer.append(byte ^ ENCRYPTION_KEY[key_index % len(ENCRYPTION_KEY)])
                    key_index += 1
                output_file.write(encrypted_buffer)
                buffer = input_file.read(4096)
    except Exception as e:
        raise IOError(f"Error al encriptar el archivo: {e}")
    return encrypted_file_path
def decrypt_file(file_path):
    # WARNING: This function uses a simple XOR cipher, which is not secure.
    # It should not be used for decrypting sensitive data.
    if not file_path.endswith(".enc"):
        raise ValueError("El archivo a descifrar debe tener la extensión .enc")
    
    original_file_path = file_path[:-4]
    decrypted_file_path = original_file_path
    
    if os.path.exists(decrypted_file_path):
        base, ext = os.path.splitext(original_file_path)
        i = 1
        while os.path.exists(decrypted_file_path):
            decrypted_file_path = f"{base}.dec({i}){ext}"
            i += 1
            
    try:
        with open(file_path, "rb") as input_file, open(decrypted_file_path, "wb") as output_file:
            buffer = input_file.read(4096)
            key_index = 0
            while buffer:
                decrypted_buffer = bytearray()
                for byte in buffer:
                    decrypted_buffer.append(byte ^ ENCRYPTION_KEY[key_index % len(ENCRYPTION_KEY)])
                    key_index += 1
                output_file.write(decrypted_buffer)
                buffer = input_file.read(4096)
    except Exception as e:
        if os.path.exists(decrypted_file_path):
            os.remove(decrypted_file_path)
        raise ValueError(f"No se pudo descifrar. La clave puede ser incorrecta o el archivo está corrupto. Error: {e}")
        
    return decrypted_file_path
from ui import App
def run_gui_app():
    app = App(APP_VERSION, check_for_updates, apply_update)
    app.set_callbacks(encrypt_text, decrypt_text, encrypt_file, decrypt_file)
    app.mainloop()

def attach_to_console():
    if os.name != 'nt':
        return
    try:
        if ctypes.windll.kernel32.AttachConsole(0xFFFFFFFF):
            sys.stdout = open('CONOUT$', 'w')
            sys.stderr = open('CONOUT$', 'w')
    except Exception:
        pass

def main():
    is_frozen = getattr(sys, 'frozen', False)
    args = sys.argv[1:]
    if "--uninstall" in args:
        if is_frozen and os.name == 'nt':
            attach_to_console()
            uninstall_application()
        elif not is_frozen:
            print("La desinstalación solo está disponible en la versión compilada de Windows.")
        else:
            print("La desinstalación solo está disponible en Windows.")
    else:
        run_gui_app()
if __name__ == "__main__":
    main()

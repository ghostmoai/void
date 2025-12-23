#!/usr/bin/env python3
"""
Script de ofuscación para EncryptorApp
Convierte archivos .py a bytecode compilado (.pyc)
"""
import py_compile
import os
import shutil
from pathlib import Path

def obfuscate_python_files():
    """Compila todos los archivos .py a .pyc"""
    
    # Archivos a ofuscar
    files_to_obfuscate = ['main.py', 'encryption.py', 'ui.py']
    
    # Crear directorio para código ofuscado
    obf_dir = Path('obfuscated')
    obf_dir.mkdir(exist_ok=True)
    
    for file in files_to_obfuscate:
        if Path(file).exists():
            print(f"Ofuscando {file}...")
            
            # Compilar a bytecode
            compiled = py_compile.compile(file, doraise=True)
            
            # Copiar el .pyc al directorio principal
            pyc_name = file.replace('.py', '.pyc')
            shutil.copy(compiled, obf_dir / pyc_name)
            
            print(f"✓ {file} → {pyc_name}")
    
    print("\n✓ Ofuscación completada")
    print("Archivos ofuscados en: obfuscated/")

if __name__ == '__main__':
    obfuscate_python_files()

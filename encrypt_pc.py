#!/usr/bin/env python3
"""
Script simple para encriptar/desencriptar archivos desde PC (línea de comandos)
Uso:
    python3 encrypt_pc.py encrypt <archivo>          # Encripta un archivo
    python3 encrypt_pc.py decrypt <archivo.enc>      # Desencripta un archivo
"""

import sys
import os
from pathlib import Path

# Importar la lógica de encriptación
import null_Encrypter_encryption as encryption_logic

def encrypt_file_cli(file_path: str):
    """Encripta un archivo desde línea de comandos"""
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo '{file_path}' no existe")
        return
    
    try:
        print(f"🔒 Encriptando: {file_path}")
        
        # Encriptar
        encrypted_data = encryption_logic.encrypt_file(file_path)
        
        # Guardar con extensión .enc
        output_path = file_path + ".enc"
        with open(output_path, "wb") as f:
            f.write(encrypted_data)
        
        print(f"✅ Archivo encriptado exitosamente!")
        print(f"📁 Guardado en: {output_path}")
        print(f"📊 Tamaño: {len(encrypted_data)} bytes")
        
        # Verificar que tiene el header
        if b"NULL_ENC_HEADER:" in encrypted_data:
            print("✅ Header de portabilidad incluido - Este archivo puede desencriptarse en cualquier dispositivo")
        
    except Exception as e:
        print(f"❌ Error al encriptar: {e}")
        import traceback
        traceback.print_exc()

def decrypt_file_cli(file_path: str):
    """Desencripta un archivo desde línea de comandos"""
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo '{file_path}' no existe")
        return
    
    try:
        print(f"🔓 Desencriptando: {file_path}")
        
        # Desencriptar
        decrypted_data = encryption_logic.decrypt_file(file_path)
        
        # Guardar sin extensión .enc
        if file_path.endswith('.enc'):
            output_path = file_path[:-4]
        else:
            output_path = file_path + ".dec"
        
        with open(output_path, "wb") as f:
            f.write(decrypted_data)
        
        print(f"✅ Archivo desencriptado exitosamente!")
        print(f"📁 Guardado en: {output_path}")
        print(f"📊 Tamaño: {len(decrypted_data)} bytes")
        
    except Exception as e:
        print(f"❌ Error al desencriptar: {e}")
        import traceback
        traceback.print_exc()

def encrypt_text_cli(text: str):
    """Encripta texto desde línea de comandos"""
    try:
        print(f"🔒 Encriptando texto...")
        encrypted = encryption_logic.encrypt_text(text)
        print(f"\n✅ Texto encriptado:")
        print(f"{encrypted}")
        print(f"\n📊 Longitud: {len(encrypted)} caracteres")
        
        # Crear carpeta null-txt si no existe
        output_dir = Path("null-txt")
        output_dir.mkdir(exist_ok=True)
        
        # Guardar en archivo dentro de null-txt
        output_file = output_dir / "encrypted_text.txt"
        with open(output_file, "w") as f:
            f.write(encrypted)
        print(f"💾 Guardado en: {output_file}")
        
    except Exception as e:
        print(f"❌ Error al encriptar: {e}")

def decrypt_text_cli(encrypted_text: str):
    """Desencripta texto desde línea de comandos"""
    try:
        print(f"🔓 Desencriptando texto...")
        decrypted = encryption_logic.decrypt_text(encrypted_text)
        print(f"\n✅ Texto desencriptado:")
        print(f"{decrypted}")
        
    except Exception as e:
        print(f"❌ Error al desencriptar: {e}")

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("🔐 null-Encrypter - Herramienta de Encriptación PC")
        print("=" * 60)
        print("\nUso:")
        print("  Archivos:")
        print("    python3 encrypt_pc.py encrypt <archivo>")
        print("    python3 encrypt_pc.py decrypt <archivo.enc>")
        print("\n  Texto:")
        print("    python3 encrypt_pc.py encrypt-text \"Tu mensaje aquí\"")
        print("    python3 encrypt_pc.py decrypt-text \"Ñn0_Mllu...\"")
        print("\nEjemplos:")
        print("    python3 encrypt_pc.py encrypt documento.pdf")
        print("    python3 encrypt_pc.py decrypt documento.pdf.enc")
        print("    python3 encrypt_pc.py encrypt-text \"Hola mundo\"")
        print("=" * 60)
        return
    
    command = sys.argv[1].lower()
    
    if command == "encrypt" and len(sys.argv) >= 3:
        encrypt_file_cli(sys.argv[2])
    elif command == "decrypt" and len(sys.argv) >= 3:
        decrypt_file_cli(sys.argv[2])
    elif command == "encrypt-text" and len(sys.argv) >= 3:
        encrypt_text_cli(sys.argv[2])
    elif command == "decrypt-text" and len(sys.argv) >= 3:
        decrypt_text_cli(sys.argv[2])
    else:
        print("❌ Comando no válido. Usa 'python3 encrypt_pc.py' para ver la ayuda.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
null-Encrypter CLI - Ejecutable Portable
Este archivo puede ejecutarse directamente sin instalación
"""

# Importar módulo de encriptación inline para portabilidad
import os
import hashlib
import base64
import re
import random
import string
from pathlib import Path
import platform
import sys
import datetime

# --- Configuración Global ---
system = platform.system()

if system == "Windows":
    APP_DATA_DIR = Path(os.getenv('APPDATA')) / "null-Encrypter"
elif system == "Linux" or system == "Darwin":
    APP_DATA_DIR = Path.home() / ".local" / "share" / "null-Encrypter"
else:
    APP_DATA_DIR = Path("./.encryptorx_data")

KEY_FILE = APP_DATA_DIR / "key.key"
NONCE_SIZE = 16

# --- Funciones de Encriptación (Inline) ---
def get_or_generate_key():
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = os.urandom(32)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

CLAVE = get_or_generate_key()

def _generate_keystream(key, nonce, length):
    keystream = b''
    counter = 0
    while len(keystream) < length:
        h = hashlib.sha256(key + nonce + counter.to_bytes(4, 'big'))
        keystream += h.digest()
        counter += 1
    return keystream[:length]

def _xor_bytes(data, keystream):
    return bytes([b ^ k for b, k in zip(data, keystream)])

def _encrypt(data: bytes, key: bytes) -> bytes:
    nonce = os.urandom(NONCE_SIZE)
    keystream = _generate_keystream(key, nonce, len(data))
    encrypted_data = _xor_bytes(data, keystream)
    return nonce + encrypted_data

def _decrypt(data_with_nonce: bytes, key: bytes) -> bytes:
    if len(data_with_nonce) < NONCE_SIZE:
        raise ValueError("Invalid encrypted data")
    nonce = data_with_nonce[:NONCE_SIZE]
    encrypted_data = data_with_nonce[NONCE_SIZE:]
    keystream = _generate_keystream(key, nonce, len(encrypted_data))
    return _xor_bytes(encrypted_data, keystream)

# Patrones de clave
KEY_PATTERNS = [
    lambda i, c: f"n{i}_{c}llu", lambda i, c: f"u{i}_{c}nll", lambda i, c: f"l{i}_{c}nul",
    lambda i, c: f"ll{i}_{c}un", lambda i, c: f"nu{i}_{c}ll", lambda i, c: f"un{i}_{c}ll",
    lambda i, c: f"ln{i}_{c}ul", lambda i, c: f"ul{i}_{c}ln", lambda i, c: f"nul{i}_{c}l",
    lambda i, c: f"lun{i}_{c}l", lambda i, c: f"a{i}_{c}e", lambda i, c: f"r{i}_{c}o",
]

KEY_REGEXES = [
    r'n(\d+)_(.)llu', r'u(\d+)_(.)nll', r'l(\d+)_(.)nul',
    r'll(\d+)_(.)un', r'nu(\d+)_(.)ll', r'un(\d+)_(.)ll',
    r'ln(\d+)_(.)ul', r'ul(\d+)_(.)ln', r'nul(\d+)_(.)l',
    r'lun(\d+)_(.)l', r'a(\d+)_(.)e', r'r(\d+)_(.)o',
]

def _embed_key_string(key_bytes: bytes) -> str:
    key_b64 = base64.urlsafe_b64encode(key_bytes).decode('utf-8')
    items = []
    for idx, char in enumerate(key_b64):
        pattern = KEY_PATTERNS[idx % len(KEY_PATTERNS)]
        items.append(pattern(idx, char))
    junk_chars = string.ascii_letters + string.digits
    for _ in range(len(items) // 2):
        junk = ''.join(random.choices(junk_chars, k=random.randint(2, 4)))
        items.append(junk)
    random.shuffle(items)
    return "".join(items)

def _extract_key_from_string(content: str) -> bytes:
    key_chars = {}
    for regex in KEY_REGEXES:
        for match in re.finditer(regex, content):
            key_chars[int(match.group(1))] = match.group(2)
    if not key_chars:
        raise ValueError("No embedded key found")
    max_idx = max(key_chars.keys())
    key_b64 = "".join(key_chars[i] for i in range(max_idx + 1))
    return base64.urlsafe_b64decode(key_b64)

def encrypt_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        data = f.read()
    key_header = _embed_key_string(CLAVE)
    header = f"NULL_ENC_HEADER:{key_header}:END_HEADER:".encode('utf-8')
    return header + _encrypt(data, CLAVE)

def decrypt_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        content = f.read()
    
    header_start = b"NULL_ENC_HEADER:"
    header_end = b":END_HEADER:"
    
    if content.startswith(header_start):
        end_idx = content.find(header_end)
        header = content[len(header_start):end_idx].decode('utf-8')
        data = content[end_idx + len(header_end):]
        key = _extract_key_from_string(header)
        return _decrypt(data, key)
    else:
        return _decrypt(content, CLAVE)

# --- CLI ---
def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("🔐 null-Encrypter v2.0.0 - CLI Portable")
        print("=" * 60)
        print("\nUso:")
        print("  python null-encrypter-portable.py encrypt <archivo>")
        print("  python null-encrypter-portable.py decrypt <archivo.enc>")
        print("\nEjemplos:")
        print("  python null-encrypter-portable.py encrypt documento.pdf")
        print("  python null-encrypter-portable.py decrypt documento.pdf.enc")
        print("=" * 60)
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "encrypt" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print(f"❌ Error: '{file_path}' no existe")
            return
        
        print(f"🔒 Encriptando: {file_path}")
        encrypted = encrypt_file(file_path)
        output = file_path + ".enc"
        
        with open(output, "wb") as f:
            f.write(encrypted)
        
        print(f"✅ Archivo encriptado: {output}")
        print(f"📊 Tamaño: {len(encrypted)} bytes")
        print("✅ Header de portabilidad incluido")
        
    elif cmd == "decrypt" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print(f"❌ Error: '{file_path}' no existe")
            return
        
        print(f"🔓 Desencriptando: {file_path}")
        decrypted = decrypt_file(file_path)
        
        output = file_path[:-4] if file_path.endswith('.enc') else file_path + ".dec"
        with open(output, "wb") as f:
            f.write(decrypted)
        
        print(f"✅ Archivo desencriptado: {output}")
        print(f"📊 Tamaño: {len(decrypted)} bytes")
    else:
        print("❌ Comando inválido")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Test cross-device encryption/decryption simulation."""

import sys
sys.path.insert(0, '.')

import null_Encrypter_encryption as encryption_logic
from pathlib import Path
import os

print("=== SIMULATING CROSS-DEVICE ENCRYPTION ===\n")

# DEVICE 1: Encrypt with its own key
print("📱 DEVICE 1 (Sender)")
print("-" * 50)
device1_key_file = Path("device1_key.key")
if device1_key_file.exists():
    device1_key_file.unlink()

encryption_logic.APP_DATA_DIR = Path(".")
encryption_logic.KEY_FILE = device1_key_file
encryption_logic.CLAVE = encryption_logic.get_or_generate_key()

test_message = "Hola mundo! 123"
print(f"Original message: {test_message}")

encrypted = encryption_logic.encrypt_text(test_message)
print(f"Encrypted ({len(encrypted)} chars)")
print(f"First 100 chars: {encrypted[:100]}...")
print()

# DEVICE 2: Try to decrypt with a DIFFERENT key
print("📱 DEVICE 2 (Receiver)")
print("-" * 50)
device2_key_file = Path("device2_key.key")
if device2_key_file.exists():
    device2_key_file.unlink()

encryption_logic.KEY_FILE = device2_key_file
encryption_logic.CLAVE = encryption_logic.get_or_generate_key()  # Different key!

print(f"Device 2 has a DIFFERENT key than Device 1")
print(f"Attempting to decrypt...")
print()

try:
    decrypted = encryption_logic.decrypt_text(encrypted)
    print(f"✅ Decrypted successfully: {decrypted}")
    
    if decrypted == test_message:
        print("✅ SUCCESS: Cross-device encryption works!")
    else:
        print("❌ FAIL: Decrypted text doesn't match")
        print(f"Expected: {test_message}")
        print(f"Got: {decrypted}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
if device1_key_file.exists():
    device1_key_file.unlink()
if device2_key_file.exists():
    device2_key_file.unlink()

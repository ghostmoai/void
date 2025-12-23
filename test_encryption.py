#!/usr/bin/env python3
"""Test script to verify encryption/decryption works correctly, including new file header logic."""

import sys
import os
import shutil
sys.path.insert(0, '.')

import null_Encrypter_encryption as encryption_logic
from pathlib import Path

# Setup
encryption_logic.APP_DATA_DIR = Path(".")
encryption_logic.KEY_FILE = Path("key.key")
# Force reload key
encryption_logic.CLAVE = encryption_logic.get_or_generate_key()

print(f"Current Key: {encryption_logic.CLAVE.hex()[:16]}...")

# --- Test 1: Text Encryption ---
print("\n--- Test 1: Text Encryption ---")
test_message = "Hello World! Testing 123"
try:
    encrypted = encryption_logic.encrypt_text(test_message)
    print(f"Encrypted Text Length: {len(encrypted)}")
    
    decrypted = encryption_logic.decrypt_text(encrypted)
    
    if decrypted == test_message:
        print("✅ SUCCESS: Text Encryption/Decryption works!")
    else:
        print("❌ FAIL: Text Decrypted text doesn't match original")
        print(f"Expected: {test_message}")
        print(f"Got: {decrypted}")
except Exception as e:
    print(f"❌ ERROR in Text Test: {e}")

# --- Test 2: File Encryption with Header ---
print("\n--- Test 2: File Encryption (Embedded Key) ---")
test_filename = "test_file.txt"
enc_filename = "test_file.txt.enc"
dec_filename = "test_file_decrypted.txt"

# Create dummy file
with open(test_filename, "w") as f:
    f.write("This is a secret file content for testing file encryption portability.")

try:
    # Encrypt
    encrypted_data = encryption_logic.encrypt_file(test_filename)
    with open(enc_filename, "wb") as f:
        f.write(encrypted_data)
    print(f"File Encrypted. Size: {len(encrypted_data)} bytes")
    
    # Verify Header exists
    if b"NULL_ENC_HEADER:" in encrypted_data:
        print("✅ Header found in encrypted file.")
    else:
        print("❌ Header NOT found in encrypted file.")

    # Decrypt (Normal)
    decrypted_data = encryption_logic.decrypt_file(enc_filename)
    with open(dec_filename, "wb") as f:
        f.write(decrypted_data)
        
    with open(dec_filename, "r") as f:
        decrypted_content = f.read()
        
    if decrypted_content == "This is a secret file content for testing file encryption portability.":
        print("✅ SUCCESS: File Encryption/Decryption works!")
    else:
        print("❌ FAIL: File content mismatch")

except Exception as e:
    print(f"❌ ERROR in File Test: {e}")
    import traceback
    traceback.print_exc()

# --- Test 3: Portability Simulation (Different Key) ---
print("\n--- Test 3: Portability Simulation ---")
# Simulate a different device by changing the global key
original_key = encryption_logic.CLAVE
encryption_logic.CLAVE = os.urandom(32) # New random key
print(f"Simulating new device with Key: {encryption_logic.CLAVE.hex()[:16]}...")

try:
    # Try to decrypt the file encrypted with the OLD key
    # This should work because the key is embedded in the header!
    decrypted_data_portable = encryption_logic.decrypt_file(enc_filename)
    
    if decrypted_data_portable.decode('utf-8') == "This is a secret file content for testing file encryption portability.":
        print("✅ SUCCESS: Portability verified! Decrypted file with DIFFERENT system key using embedded header.")
    else:
        print("❌ FAIL: Portability failed. Content mismatch.")

except Exception as e:
    print(f"❌ FAIL: Portability failed with error: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
encryption_logic.CLAVE = original_key # Restore
if os.path.exists(test_filename): os.remove(test_filename)
if os.path.exists(enc_filename): os.remove(enc_filename)
if os.path.exists(dec_filename): os.remove(dec_filename)

print("\n✅ All tests completed!")

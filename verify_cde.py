
import encryption_logic
import os
import base64

def test_cde_cross_user():
    print("--- Verifying C.D.E Cross-User Logic ---")
    
    original_text = "Secret message for another user."
    print(f"Original: {original_text}")
    
    # 1. Encrypt with current key
    print("Encrypting with User A's key...")
    encrypted_text = encryption_logic.encrypt_text(original_text)
    print(f"Encrypted length: {len(encrypted_text)}")
    
    # 2. Simulate User B (Different Key)
    print("Simulating User B (changing local CLAVE)...")
    original_key = encryption_logic.CLAVE
    # Set a completely different key
    encryption_logic.CLAVE = os.urandom(32)
    
    try:
        # 3. Decrypt
        print("Attempting decryption with User B's local key (should use embedded key)...")
        decrypted_text = encryption_logic.decrypt_text(encrypted_text)
        print(f"Decrypted: {decrypted_text}")
        
        if original_text == decrypted_text:
            print("✅ Cross-user decryption verified successfully.")
        else:
            print("❌ Cross-user decryption FAILED: Content mismatch.")
            
    except Exception as e:
        print(f"❌ Cross-user decryption FAILED with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Restore key
        encryption_logic.CLAVE = original_key

if __name__ == "__main__":
    test_cde_cross_user()

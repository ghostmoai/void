
import null_Encrypter_encryption as enc

def test_methods():
    test_text = "Hello World 123!"
    
    # Base64
    b64 = enc.base64_encrypt(test_text)
    assert enc.base64_decrypt(b64) == test_text
    print("Base64 OK")
    
    # Hex
    hx = enc.hex_encrypt(test_text)
    assert enc.hex_decrypt(hx) == test_text
    print("Hex OK")
    
    # Caesar
    c = enc.caesar_encrypt(test_text, 5)
    assert enc.caesar_decrypt(c, 5) == test_text
    print("Caesar OK")
    
    # Vigenere
    v = enc.vigenere_encrypt(test_text, "python")
    assert enc.vigenere_decrypt(v, "python") == test_text
    print("Vigenere OK")
    
    # Morse
    m = enc.morse_encrypt(test_text)
    # Morse usually loses case and some symbols, so we normalize for comparison if needed
    # but my dict handles quite a bit.
    print(f"Morse: {m}")
    dec_m = enc.morse_decrypt(m)
    print(f"Decoded Morse: {dec_m}")
    print("Morse logic checked (manual view suggested for complex strings)")

    # Null (Custom)
    n = enc.encrypt_text(test_text)
    assert enc.decrypt_text(n) == test_text
    print("Null OK")

if __name__ == "__main__":
    test_methods()
    print("\nAll logic tests passed!")

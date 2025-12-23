"""
Custom encryption and decryption logic for the EncryptorX application.
"""
import os
import hashlib
import base64
import re
import random
import string
from pathlib import Path
import platform

# --- Global Configuration ---
system = platform.system()

if system == "Windows":
    APP_DATA_DIR = Path("C:/null/EncryptorApp")
elif system == "Linux" or system == "Darwin":
    # Use standard XDG data home or similar
    APP_DATA_DIR = Path.home() / ".local" / "share" / "null-Encrypter"
else:
    # Fallback (e.g. Android default before Kivy overrides it, or simple script usage)
    APP_DATA_DIR = Path("./.encryptorx_data")

KEY_FILE = APP_DATA_DIR / "key.key"
NONCE_SIZE = 16  # 128-bit nonce for security

# --- Key Management ---
def get_or_generate_key():
    """Get the encryption key from file, or generate a new one if it doesn't exist."""
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            return f.read()
    
    # Generate a strong 256-bit (32-byte) key
    key = os.urandom(32)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

CLAVE = get_or_generate_key()

# --- Core Stream Cipher Logic ---
def _generate_keystream(key, nonce, length):
    """
    Generates a pseudo-random keystream of a given length.
    Uses HMAC-SHA256 for a secure derivation of the stream from the key and nonce.
    """
    keystream = b''
    counter = 0
    while len(keystream) < length:
        # Combine key, nonce, and a counter to generate unique stream blocks
        h = hashlib.sha256(key + nonce + counter.to_bytes(4, 'big'))
        keystream += h.digest()
        counter += 1
    return keystream[:length]

def _xor_bytes(data, keystream):
    """Performs a bitwise XOR operation between two byte strings."""
    return bytes([b ^ k for b, k in zip(data, keystream)])

def _encrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypts data using the custom stream cipher.
    A random nonce is generated and prepended to the ciphertext.
    """
    nonce = os.urandom(NONCE_SIZE)
    keystream = _generate_keystream(key, nonce, len(data))
    encrypted_data = _xor_bytes(data, keystream)
    # The nonce is essential for decryption, so it's stored with the data
    return nonce + encrypted_data

def _decrypt(data_with_nonce: bytes, key: bytes) -> bytes:
    """
    Decrypts data using the custom stream cipher.
    Extracts the nonce from the beginning of the data.
    """
    if len(data_with_nonce) < NONCE_SIZE:
        raise ValueError("Invalid encrypted data: too short to contain a nonce.")
    
    nonce = data_with_nonce[:NONCE_SIZE]
    encrypted_data = data_with_nonce[NONCE_SIZE:]
    keystream = _generate_keystream(key, nonce, len(encrypted_data))
    decrypted_data = _xor_bytes(encrypted_data, keystream)
    return decrypted_data

# --- Pattern Logic for Key Embedding ---
# These are the signature "Null" patterns
KEY_PATTERNS = [
    lambda i, c: f"n{i}_{c}llu", lambda i, c: f"u{i}_{c}nll", lambda i, c: f"l{i}_{c}nul",
    lambda i, c: f"ll{i}_{c}un", lambda i, c: f"nu{i}_{c}ll", lambda i, c: f"un{i}_{c}ll",
    lambda i, c: f"ln{i}_{c}ul", lambda i, c: f"ul{i}_{c}ln", lambda i, c: f"nul{i}_{c}l",
    lambda i, c: f"lun{i}_{c}l", lambda i, c: f"a{i}_{c}e",   lambda i, c: f"r{i}_{c}o",
    lambda i, c: f"e{i}_{c}a",   lambda i, c: f"o{i}_{c}r",   lambda i, c: f"i{i}_{c}u",
    lambda i, c: f"s{i}_{c}t",   lambda i, c: f"t{i}_{c}s",   lambda i, c: f"m{i}_{c}n",
    lambda i, c: f"p{i}_{c}q",   lambda i, c: f"d{i}_{c}b",   lambda i, c: f"f{i}_{c}g",
    lambda i, c: f"h{i}_{c}j",   lambda i, c: f"k{i}_{c}v",   lambda i, c: f"w{i}_{c}x",
    lambda i, c: f"y{i}_{c}z",   lambda i, c: f"c{i}_{c}d",   lambda i, c: f"g{i}_{c}h",
    lambda i, c: f"j{i}_{c}k",   lambda i, c: f"v{i}_{c}w",   lambda i, c: f"x{i}_{c}y",
]

KEY_REGEXES = [
    r'n(\d+)_(.)llu', r'u(\d+)_(.)nll', r'l(\d+)_(.)nul',
    r'll(\d+)_(.)un', r'nu(\d+)_(.)ll', r'un(\d+)_(.)ll',
    r'ln(\d+)_(.)ul', r'ul(\d+)_(.)ln', r'nul(\d+)_(.)l',
    r'lun(\d+)_(.)l', r'a(\d+)_(.)e',   r'r(\d+)_(.)o',
    r'e(\d+)_(.)a',   r'o(\d+)_(.)r',   r'i(\d+)_(.)u',
    r's(\d+)_(.)t',   r't(\d+)_(.)s',   r'm(\d+)_(.)n',
    r'p(\d+)_(.)q',   r'd(\d+)_(.)b',   r'f(\d+)_(.)g',
    r'h(\d+)_(.)j',   r'k(\d+)_(.)v',   r'w(\d+)_(.)x',
    r'y(\d+)_(.)z',   r'c(\d+)_(.)d',   r'g(\d+)_(.)h',
    r'j(\d+)_(.)k',   r'v(\d+)_(.)w',   r'x(\d+)_(.)y',
]

DATA_PATTERNS = [
    lambda i, c: f"N{i}_{c}LLU", lambda i, c: f"U{i}_{c}NLL", lambda i, c: f"L{i}_{c}NUL",
    lambda i, c: f"LL{i}_{c}UN", lambda i, c: f"NU{i}_{c}LL", lambda i, c: f"UN{i}_{c}LL",
    lambda i, c: f"LN{i}_{c}UL", lambda i, c: f"UL{i}_{c}LN", lambda i, c: f"NUL{i}_{c}L",
    lambda i, c: f"LUN{i}_{c}L", lambda i, c: f"A{i}_{c}E",   lambda i, c: f"R{i}_{c}O",
    lambda i, c: f"E{i}_{c}A",   lambda i, c: f"O{i}_{c}R",   lambda i, c: f"I{i}_{c}U",
    lambda i, c: f"S{i}_{c}T",   lambda i, c: f"T{i}_{c}S",   lambda i, c: f"M{i}_{c}N",
    lambda i, c: f"P{i}_{c}Q",   lambda i, c: f"D{i}_{c}B",   lambda i, c: f"F{i}_{c}G",
    lambda i, c: f"H{i}_{c}J",   lambda i, c: f"K{i}_{c}V",   lambda i, c: f"W{i}_{c}X",
    lambda i, c: f"Y{i}_{c}Z",   lambda i, c: f"C{i}_{c}D",   lambda i, c: f"G{i}_{c}H",
    lambda i, c: f"J{i}_{c}K",   lambda i, c: f"V{i}_{c}W",   lambda i, c: f"X{i}_{c}Y",
]

DATA_REGEXES = [
    r'N(\d+)_(.)LLU', r'U(\d+)_(.)NLL', r'L(\d+)_(.)NUL',
    r'LL(\d+)_(.)UN', r'NU(\d+)_(.)LL', r'UN(\d+)_(.)LL',
    r'LN(\d+)_(.)UL', r'UL(\d+)_(.)LN', r'NUL(\d+)_(.)L',
    r'LUN(\d+)_(.)L', r'A(\d+)_(.)E',   r'R(\d+)_(.)O',
    r'E(\d+)_(.)A',   r'O(\d+)_(.)R',   r'I(\d+)_(.)U',
    r'S(\d+)_(.)T',   r'T(\d+)_(.)S',   r'M(\d+)_(.)N',
    r'P(\d+)_(.)Q',   r'D(\d+)_(.)B',   r'F(\d+)_(.)G',
    r'H(\d+)_(.)J',   r'K(\d+)_(.)V',   r'W(\d+)_(.)X',
    r'Y(\d+)_(.)Z',   r'C(\d+)_(.)D',   r'G(\d+)_(.)H',
    r'J(\d+)_(.)K',   r'V(\d+)_(.)W',   r'X(\d+)_(.)Y',
]

def _embed_key_string(key_bytes: bytes) -> str:
    """Creates a string containing the key dispersed with patterns."""
    key_b64 = base64.urlsafe_b64encode(key_bytes).decode('utf-8')
    items = []
    for idx, char in enumerate(key_b64):
        pattern = KEY_PATTERNS[idx % len(KEY_PATTERNS)]
        items.append(pattern(idx, char))
    
    # Add some noise to the key header too
    junk_chars = string.ascii_letters + string.digits
    for _ in range(len(items) // 2):
        junk_len = random.randint(2, 4)
        junk = ''.join(random.choices(junk_chars, k=junk_len))
        items.append(junk)
        
    random.shuffle(items)
    return "".join(items)

def _extract_key_from_string(content: str) -> bytes:
    """Extracts the key from a string using patterns."""
    key_chars = {}
    for regex in KEY_REGEXES:
        matches = re.finditer(regex, content)
        for match in matches:
            key_chars[int(match.group(1))] = match.group(2)
            
    if not key_chars:
        raise ValueError("No embedded key found.")
        
    max_key_idx = max(key_chars.keys())
    reconstructed_key_b64 = ""
    for i in range(max_key_idx + 1):
        if i not in key_chars:
            raise ValueError(f"Incomplete key data. Missing character at position {i}.")
        reconstructed_key_b64 += key_chars[i]
        
    return base64.urlsafe_b64decode(reconstructed_key_b64)

# --- Public API for Text Encryption ---
def encrypt_text(text: str) -> str:
    """Encrypts a string with heavily obfuscated embedded key and data dispersed throughout."""
    if not text:
        return ""
    data_bytes = text.encode('utf-8')
    encrypted_bytes = _encrypt(data_bytes, CLAVE)
    encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
    
    items = []
    
    # 1. Embed Key (using shared logic, but we want it mixed in for text)
    # We manually do it here to mix it with data in the same list
    key_b64 = base64.urlsafe_b64encode(CLAVE).decode('utf-8')
    for idx, char in enumerate(key_b64):
        pattern = KEY_PATTERNS[idx % len(KEY_PATTERNS)]
        items.append(pattern(idx, char))
        
    # 2. Embed Data
    for idx, char in enumerate(encrypted_b64):
        pattern = DATA_PATTERNS[idx % len(DATA_PATTERNS)]
        items.append(pattern(idx, char))
        
    # 3. Add Noise (Junk)
    junk_chars = string.ascii_letters + string.digits
    
    # Add significant noise (50-100% of data length)
    num_junk = len(items)
    for _ in range(num_junk):
        junk_len = random.randint(2, 6)
        junk = ''.join(random.choices(junk_chars, k=junk_len))
        items.append(junk)
        
    # Shuffle everything
    random.shuffle(items)
    
    # Add prefix
    result = 'Ñ' + ''.join(items)
    return result

def decrypt_text(b64_encrypted_text: str) -> str:
    """Decrypts a string with heavily obfuscated dispersed key extraction."""
    if not b64_encrypted_text:
        return ""
    
    try:
        # Sanitize input: remove whitespace and normalize
        obfuscated_text = b64_encrypted_text.strip()
        obfuscated_text = ''.join(obfuscated_text.split())
        
        # Check if message has embedded key (starts with Ñ)
        if obfuscated_text.startswith('Ñ'):
            # Remove Ñ prefix
            content = obfuscated_text[1:]
            
            # --- Extract Key ---
            embedded_key = _extract_key_from_string(content)
            
            # --- Extract Data ---
            data_chars = {}
            for regex in DATA_REGEXES:
                matches = re.finditer(regex, content)
                for match in matches:
                    data_chars[int(match.group(1))] = match.group(2)
            
            if not data_chars:
                raise ValueError("No encrypted data found. The message may be corrupted.")
                
            max_data_idx = max(data_chars.keys())
            encrypted_message = ""
            for i in range(max_data_idx + 1):
                if i not in data_chars:
                    raise ValueError(f"Incomplete message data. Missing character at position {i}.")
                encrypted_message += data_chars[i]
            
            # Decrypt
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_message)
            decrypted_bytes = _decrypt(encrypted_bytes, embedded_key)
            return decrypted_bytes.decode('utf-8')
            
        else:
            # Old format: use default key
            encrypted_bytes = base64.urlsafe_b64decode(obfuscated_text)
            decrypted_bytes = _decrypt(encrypted_bytes, CLAVE)
            return decrypted_bytes.decode('utf-8')
            
    except (ValueError, base64.binascii.Error) as e:
        raise ValueError(f"Decryption failed: {str(e)}") from e

# --- Public API for File Encryption ---
def encrypt_file(file_path: str) -> bytes:
    """
    Encrypts a file's content and returns the encrypted data as bytes.
    NOW INCLUDES EMBEDDED KEY HEADER for portability.
    Format: b'NULL_ENC_HEADER:' + utf8_encoded_obfuscated_key + b':END_HEADER:' + binary_encrypted_data
    """
    # Safety check for very large files
    file_size = os.path.getsize(file_path)
    if file_size > 500 * 1024 * 1024:  # 500 MB limit
        raise ValueError("File is too large to encrypt (limit: 500MB).")

    try:
        with open(file_path, "rb") as infile:
            file_data = infile.read()
        
        # 1. Generate Key Header
        # We use the same obfuscation style as text for the key
        key_header_str = _embed_key_string(CLAVE)
        full_header = f"NULL_ENC_HEADER:{key_header_str}:END_HEADER:".encode('utf-8')
        
        # 2. Encrypt Content
        encrypted_content = _encrypt(file_data, CLAVE)
        
        return full_header + encrypted_content

    except IOError as e:
        raise IOError(f"Error reading file for encryption: {e}") from e

def decrypt_file(encrypted_file_path: str) -> bytes:
    """
    Decrypts a file's content and returns the decrypted data as bytes.
    Supports both legacy (key file) and new (embedded key) formats.
    """
    if not encrypted_file_path.endswith(".enc"):
        print("Warning: Selected file for decryption does not end with .enc")

    try:
        with open(encrypted_file_path, "rb") as infile:
            file_content = infile.read()

        # Check for new format with header
        header_start = b"NULL_ENC_HEADER:"
        header_end = b":END_HEADER:"
        
        if file_content.startswith(header_start):
            try:
                # Extract Header
                end_idx = file_content.find(header_end)
                if end_idx == -1:
                    raise ValueError("Corrupt file header.")
                
                header_content = file_content[len(header_start):end_idx].decode('utf-8')
                encrypted_data = file_content[end_idx + len(header_end):]
                
                # Extract Key from Header
                embedded_key = _extract_key_from_string(header_content)
                
                # Decrypt
                return _decrypt(encrypted_data, embedded_key)
                
            except Exception as e:
                print(f"Header decryption failed, trying legacy method: {e}")
                # Fallback to legacy if header parsing fails (unlikely if format is correct)
                return _decrypt(file_content, CLAVE)
        else:
            # Legacy format (no header, uses system key)
            return _decrypt(file_content, CLAVE)

    except (IOError, ValueError) as e:
        raise ValueError(f"Could not decrypt. Key might be incorrect or file is corrupt. Error: {e}") from e
# --- New Encryption Methods ---

def base64_encrypt(text: str) -> str:
    """Standard Base64 encoding."""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def base64_decrypt(text: str) -> str:
    """Standard Base64 decoding."""
    try:
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        raise ValueError("Invalid Base64 data")

def hex_encrypt(text: str) -> str:
    """Standard Hexadecimal encoding."""
    return text.encode('utf-8').hex()

def hex_decrypt(text: str) -> str:
    """Standard Hexadecimal decoding."""
    try:
        return bytes.fromhex(text).decode('utf-8')
    except Exception:
        raise ValueError("Invalid Hexadecimal data")

def caesar_encrypt(text: str, shift: int) -> str:
    """Caesar Cipher encryption."""
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def caesar_decrypt(text: str, shift: int) -> str:
    """Caesar Cipher decryption."""
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text: str, key: str) -> str:
    """Vigenère Cipher encryption."""
    if not key: return text
    result = ""
    key = key.lower()
    key_idx = 0
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_idx % len(key)]) - ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
            key_idx += 1
        else:
            result += char
    return result

def vigenere_decrypt(text: str, key: str) -> str:
    """Vigenère Cipher decryption."""
    if not key: return text
    result = ""
    key = key.lower()
    key_idx = 0
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_idx % len(key)]) - ord('a')
            result += chr((ord(char) - start - shift) % 26 + start)
            key_idx += 1
        else:
            result += char
    return result

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}
REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def morse_encrypt(text: str) -> str:
    """Morse Code encryption."""
    text = text.upper()
    return " ".join(MORSE_CODE_DICT.get(char, char) for char in text)

def morse_decrypt(text: str) -> str:
    """Morse Code decryption."""
    words = text.split(" / ")
    decoded_words = []
    for word in words:
        chars = word.split()
        decoded_words.append("".join(REVERSE_MORSE_DICT.get(c, c) for c in chars))
    return " ".join(decoded_words)

#!/usr/bin/env python3
"""
fuerza.py - AI-Powered Brute Force Decryption Tool for null-Encrypter
Author: el_tio_null <encryternull@gmail.com>

Advanced decryption tool that uses multiple intelligent methods to crack encrypted messages.
Logs all attempts and measures performance.
"""

import sys
import os
import time
import datetime
import hashlib
import string
import random
import multiprocessing 
import concurrent.futures 
import itertools # Mantenido del original, aunque no se usa en los métodos finales

# Asegurarse de que la lógica de encriptación esté disponible
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import null_Encrypter_encryption as encryption_logic
from pathlib import Path


# ==============================================================================
# CONFIGURACIÓN (SIN LÍMITES)
# ==============================================================================
TIME_LIMIT_SECONDS = float('inf') # Límite de tiempo: Infinito
BRUTE_FORCE_ATTEMPTS = 10**15 # Límite de intentos: 1 Cuatrillón (efectivamente ilimitado)
# ==============================================================================


# ==============================================================================
# FUNCIÓN TRABAJADORA GLOBAL PARA PROCESOS PARALELOS
# (Necesaria para concurrent.futures.ProcessPoolExecutor)
# ==============================================================================
def _worker_decrypt_key(task_data):
    """
    Intenta descifrar con una clave en un proceso separado.
    """
    encrypted_text, key_bytes, original_key_bytes = task_data
    
    try:
        # Reemplazar la clave temporalmente de forma segura
        temp_original_clave = encryption_logic.CLAVE
        encryption_logic.CLAVE = key_bytes
        decrypted = encryption_logic.decrypt_text(encrypted_text)
        encryption_logic.CLAVE = temp_original_clave
        
        # Éxito: devolver la clave y el resultado
        return key_bytes.decode('utf-8', errors='ignore'), decrypted
        
    except Exception:
        # Fallo: devolver None
        return None, None

# ==============================================================================


class DecryptionLogger:
    """Logs all decryption attempts and results."""
    
    def __init__(self, log_file: str = "decryption_log.txt"):
        self.log_file = log_file
        self.start_time = time.time()
        self.attempts = 0
        self.methods_tried = []
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("null-Encrypter AI Decryption Log\n")
            f.write(f"Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("MODE: UNLIMITED ATTEMPTS (Will run until key is found or manually stopped)\n")
            f.write("=" * 80 + "\n\n")
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        elapsed = time.time() - self.start_time
        timestamp = f"[{elapsed:8.2f}s]"
        log_line = f"{timestamp} [{level:7s}] {message}\n"
        
        print(log_line.strip())
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def log_attempt(self, method: str, key_info: str, success: bool, result: str = ""):
        """Log a decryption attempt."""
        self.attempts += 1
        status = "✅ SUCCESS" if success else "❌ FAILED"
        
        self.log(f"Attempt #{self.attempts} | Method: {method} | Key: {key_info} | {status}", 
                 "SUCCESS" if success else "ATTEMPT")
        
        if success:
            self.log(f"Decrypted text: {result[:100]}{'...' if len(result) > 100 else ''}", "RESULT")
    
    def log_method_start(self, method_name: str, description: str):
        """Log the start of a new method."""
        self.methods_tried.append(method_name)
        self.log(f"\n{'='*60}", "METHOD")
        self.log(f"Starting Method: {method_name}", "METHOD")
        self.log(f"Description: {description}", "METHOD")
        self.log(f"{'='*60}", "METHOD")
    
    def finalize(self, success: bool, key_used: str = None, method_used: str = None):
        """Finalize the log with summary."""
        elapsed = time.time() - self.start_time
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write("DECRYPTION SUMMARY\n")
            f.write("=" * 80 + "\n")
            
            if success:
                f.write("Status: SUCCESS ✅\n")
            else:
                # Indica que falló o fue detenido manualmente mientras corría la fuerza bruta ilimitada
                f.write("Status: RUNNING 🔄 (Manually stopped or failed initial methods)\n") 
                
            f.write(f"Total Attempts: {self.attempts}\n")
            f.write(f"Methods Tried: {len(self.methods_tried)}\n")
            f.write(f"Time Elapsed: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)\n")
            
            if success:
                f.write(f"Successful Method: {method_used}\n")
                f.write(f"Key Used: {key_used}\n")
            
            f.write("\nMethods Attempted:\n")
            for i, method in enumerate(self.methods_tried, 1):
                f.write(f"  {i}. {method}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Finished: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")


class AIDecryptor:
    """AI-powered decryption engine."""
    
    def __init__(self, encrypted_text: str, logger: DecryptionLogger):
        self.encrypted_text = encrypted_text
        self.logger = logger
        self.original_key = encryption_logic.CLAVE
    
    def try_decrypt(self, key: bytes, method: str, key_info: str) -> tuple[bool, str]:
        """Try to decrypt with a specific key."""
        try:
            # Temporarily override the key
            encryption_logic.CLAVE = key
            decrypted = encryption_logic.decrypt_text(self.encrypted_text)
            encryption_logic.CLAVE = self.original_key
            
            self.logger.log_attempt(method, key_info, True, decrypted)
            return True, decrypted
        except Exception as e:
            encryption_logic.CLAVE = self.original_key
            self.logger.log_attempt(method, key_info, False, str(e))
            return False, str(e)
    
    def method_1_embedded_key(self) -> tuple[bool, str, str]:
        """Method 1: Try with embedded key (standard approach)."""
        self.logger.log_method_start(
            "Embedded Key Extraction",
            "Attempts to extract and use the key embedded in the encrypted message"
        )
        try:
            decrypted = encryption_logic.decrypt_text(self.encrypted_text)
            self.logger.log_attempt("Embedded Key", "Extracted from message", True, decrypted)
            return True, decrypted, "Embedded key from message"
        except Exception as e:
            self.logger.log_attempt("Embedded Key", "Extracted from message", False, str(e))
            return False, "", ""
    
    def method_2_default_key(self) -> tuple[bool, str, str]:
        """Method 2: Try with default system key."""
        self.logger.log_method_start(
            "Default System Key",
            "Attempts decryption using the default system key"
        )
        success, result = self.try_decrypt(
            self.original_key,
            "Default Key",
            self.original_key.decode('utf-8', errors='ignore')[:32]
        )
        if success:
            return True, result, self.original_key.decode('utf-8', errors='ignore')
        return False, "", ""
    
    def method_3_common_keys(self) -> tuple[bool, str, str]:
        """Method 3: Try common/predictable keys."""
        self.logger.log_method_start(
            "Common Keys Database",
            "Testing against a database of commonly used encryption keys"
        )
        common_keys = [
            (b"0123456789ABCDEF0123456789ABCDEF", "Sequential hex"),
            (b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "All A's"),
            (b"00000000000000000000000000000000", "All zeros"),
            (b"11111111111111111111111111111111", "All ones"),
            (b"password1234567890password123456", "Password pattern"),
            (b"nullencrypternullencrypternullen", "App name"),
            (b"admin123admin123admin123admin123", "Admin pattern"),
            (b"qwertyuiopqwertyuiopqwertyuiopqw", "Keyboard pattern"),
        ]
        for key, description in common_keys:
            success, result = self.try_decrypt(key, "Common Key", f"{description}: {key.decode('utf-8', errors='ignore')}")
            if success:
                return True, result, key.decode('utf-8', errors='ignore')
        return False, "", ""
    
    def method_4_pattern_analysis(self) -> tuple[bool, str, str]:
        """Method 4: Analyze message patterns and generate keys."""
        self.logger.log_method_start(
            "Pattern Analysis",
            "Analyzes the encrypted message structure to generate potential keys"
        )
        patterns = []
        text_hash = hashlib.sha256(self.encrypted_text.encode()).hexdigest()[:32]
        patterns.append((text_hash.encode(), "SHA256 hash of encrypted text"))
        text_md5 = hashlib.md5(self.encrypted_text.encode()).hexdigest()
        patterns.append((text_md5.encode(), "MD5 hash of encrypted text"))
        if len(self.encrypted_text) >= 32:
            pattern_key = self.encrypted_text[:32].encode('utf-8', errors='ignore')
            patterns.append((pattern_key, "First 32 chars of encrypted text"))
        for key, description in patterns:
            key = (key * 32)[:32]
            success, result = self.try_decrypt(key, "Pattern Analysis", description)
            if success:
                return True, result, key.decode('utf-8', errors='ignore')
        return False, "", ""
    
    def method_5_dictionary_attack(self, max_words: int = 1000) -> tuple[bool, str, str]:
        """Method 5: Dictionary attack with common words."""
        self.logger.log_method_start(
            "Dictionary Attack",
            f"Testing up to {max_words} common words and phrases"
        )
        common_words = [
            "password", "admin", "root", "user", "test", "demo", "secret",
            "encryption", "decryption", "null", "encrypter", "key", "master",
            "default", "system", "private", "public", "secure", "crypto",
            "android", "mobile", "app", "application", "data", "file",
            "message", "text", "code", "hash", "salt", "pepper",
        ]
        variations = []
        for word in common_words[:20]:
            variations.append(word)
            variations.append(word.upper())
            variations.append(word.capitalize())
            variations.append(word + "123")
            variations.append(word + "2024")
            variations.append(word + "2025")
        for word in variations[:max_words]:
            key = (word * 32)[:32].encode('utf-8', errors='ignore')
            success, result = self.try_decrypt(key, "Dictionary", f"Word: {word}")
            if success:
                return True, result, word
        return False, "", ""

    # MÉTODO 6: FUERZA BRUTA PARALELA E ILIMITADA CON PISTAS ('ñ' y '12')
    def method_6_brute_force_parallel(self, max_attempts: int = BRUTE_FORCE_ATTEMPTS) -> tuple[bool, str, str]:
        """Method 6: Parallel Brute force (UNLIMITED ATTEMPTS) with 'ñ' start and '12' end clues."""
        self.logger.log_method_start(
            "Brute Force (PARALLEL - ILIMITADO)",
            f"Attempting up to 10^15 keys, starting with **ñ** and ending with **12**, using all available CPU cores."
        )
        
        charset = string.ascii_letters + string.digits
        tasks = []
        
        # 1. Generar todas las tareas (claves) hasta el límite virtual
        for i in range(max_attempts):
            
            # --- IMPLEMENTACIÓN DE LAS PISTAS: Empieza con 'ñ' y termina con '12' ---
            first_char = 'ñ'
            # 29 caracteres centrales, aleatorios (32 - 1 - 2 = 29)
            remaining_chars = ''.join(random.choices(charset, k=29))
            last_chars = '12'
            
            random_key = first_char + remaining_chars + last_chars
            key_bytes = random_key.encode('utf-8') 
            # -----------------------------------
            
            tasks.append((self.encrypted_text, key_bytes, self.original_key))
            self.logger.attempts += 1 
            
            if i % 1000000 == 0 and i > 0:
                self.logger.log(f"Generated: {i} / {BRUTE_FORCE_ATTEMPTS} keys", "PROGRESS")


        # 2. Ejecutar las tareas en paralelo usando todos los núcleos
        num_cores = multiprocessing.cpu_count()
        self.logger.log(f"Starting parallel execution using ALL {num_cores} cores...", "INFO")

        try:
            # max_workers=None asegura que se usen todos los núcleos de la CPU
            with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executor:
                # No se establece timeout, corre ilimitadamente hasta encontrar o terminar las tareas
                results = executor.map(_worker_decrypt_key, tasks) 

                # 3. Procesar resultados
                for key, decrypted in results:
                    if key is not None:
                        self.logger.log_attempt("Brute Force (PARALLEL)", f"Key: {key}", True, decrypted)
                        executor.shutdown(wait=False, cancel_futures=True) # Detener otros procesos
                        return True, decrypted, key
        
        except Exception as e:
            self.logger.log(f"An error occurred during parallel execution: {e}", "ERROR")
            
        return False, "", ""
    
    # NUEVO MÉTODO 7: PATRÓN PERSONALIZADO (n{i}_{c}llu)
    def method_7_custom_pattern(self) -> tuple[bool, str, str]:
        """Method 7: Try custom pattern n{i}_{c}llu with padding."""
        self.logger.log_method_start(
            "Custom Pattern Attack",
            "Testing patterns based on 'n{i}_{c}llu' where i, c are digits 0-9."
        )
        
        digits = string.digits # '0123456789'
        
        for i in digits:
            for c in digits:
                base_pattern = f"n{i}_{c}llu" # 7 caracteres
                
                # Variación 1: Relleno con ceros para 32 bytes
                key_str_v1 = (base_pattern + '0' * 32)[:32]
                key_v1 = key_str_v1.encode('utf-8')
                success, result = self.try_decrypt(key_v1, "Custom Pattern (V1)", f"Padding V1: {key_str_v1}")
                if success:
                    return True, result, key_str_v1

                # Variación 2: Repetir el patrón para 32 bytes
                key_str_v2 = (base_pattern * 5)[:32]
                key_v2 = key_str_v2.encode('utf-8')
                success, result = self.try_decrypt(key_v2, "Custom Pattern (V2)", f"Repeating V2: {key_str_v2}")
                if success:
                    return True, result, key_str_v2
        
        return False, "", ""
    
    # Otros métodos adicionales para mayor robustez
    
    def method_8_date_based_keys(self) -> tuple[bool, str, str]:
        """Method 8: Date-Based Keys."""
        self.logger.log_method_start(
            "Date-Based Keys",
            "Testing keys based on common date formats (e.g., year, date, month)"
        )
        current_year = datetime.datetime.now().year
        dates_to_try = [
            str(current_year), str(current_year - 1), "2020", "2021", "2022", "2023", "2024", "1990",
            "0101", "1231", "1111", "0000",
        ]
        for date_str in dates_to_try:
            key_base = date_str * 8
            key = (key_base * 32)[:32].encode('utf-8', errors='ignore')
            success, result = self.try_decrypt(key, "Date Key", f"Pattern: {date_str}")
            if success:
                return True, result, key.decode('utf-8', errors='ignore')
        return False, "", ""
        
    def method_9_sequential_patterns(self) -> tuple[bool, str, str]:
        """Method 9: Sequential Patterns."""
        self.logger.log_method_start(
            "Sequential Patterns",
            "Testing simple, repeating character patterns (a, b, 1, 2, ...)"
        )
        patterns = [
            (b"12345678123456781234567812345678", "1-8 repeating"),
            (b"AAAAAAAAABBBBBBBBCCCCCCCCCDDDDDDDD", "A,B,C,D blocks"),
            (b"!@#$%^&*!@#$%^&*!@#$%^&*!@#$%^&*", "Special chars repeating"),
            (b"zyxwuvtszyxwuvtszyxwuvtszyxwuvts", "Reverse alphabet"),
        ]
        for key, description in patterns:
            success, result = self.try_decrypt(key, "Sequential Pattern", description)
            if success:
                return True, result, key.decode('utf-8', errors='ignore')
        return False, "", ""
        
    def method_10_key_rotation(self) -> tuple[bool, str, str]:
        """Method 10: Key Rotation/Shift."""
        self.logger.log_method_start(
            "Key Rotation/Shift",
            "Tests simple 1-byte shifts or rotations of the Default Key and Common Keys"
        )
        base_keys = [
            (self.original_key, "Default Key"),
            (b"0123456789ABCDEF0123456789ABCDEF", "Common Key 1"),
        ]
        for base_key, base_desc in base_keys:
            rotated_key = base_key[1:] + base_key[:1]
            desc = f"Shifted {base_desc} (1-byte left)"
            success, result = self.try_decrypt(rotated_key, "Key Rotation", desc)
            if success:
                return True, result, rotated_key.decode('utf-8', errors='ignore')
            rotated_key = base_key[-1:] + base_key[:-1]
            desc = f"Shifted {base_desc} (1-byte right)"
            success, result = self.try_decrypt(rotated_key, "Key Rotation", desc)
            if success:
                return True, result, rotated_key.decode('utf-8', errors='ignore')
        return False, "", ""


    def run_all_methods(self) -> tuple[bool, str, str, str]:
        """Run all decryption methods in sequence."""
        self.logger.log("Starting AI-powered decryption process...", "START")
        self.logger.log(f"Encrypted text length: {len(self.encrypted_text)} characters", "INFO")
        self.logger.log(f"First 50 chars: {self.encrypted_text[:50]}...", "INFO")
        
        methods = [
            ("Embedded Key", self.method_1_embedded_key),
            ("Default Key", self.method_2_default_key),
            ("Common Keys", self.method_3_common_keys),
            ("Pattern Analysis", self.method_4_pattern_analysis),
            ("Dictionary Attack", self.method_5_dictionary_attack),
            ("Brute Force (PARALLEL)", self.method_6_brute_force_parallel), # Ilimitada con pistas 'ñ' y '12'
            ("Custom Pattern (n{i}_{c}llu)", self.method_7_custom_pattern), # Nuevo método
            ("Date-Based Keys", self.method_8_date_based_keys),
            ("Sequential Patterns", self.method_9_sequential_patterns),
            ("Key Rotation/Shift", self.method_10_key_rotation),
        ]
        
        for method_name, method_func in methods:
            try:
                success, decrypted, key_used = method_func()
            except Exception:
                continue
                
            if success:
                self.logger.log(f"\n🎉 DECRYPTION SUCCESSFUL! 🎉", "SUCCESS")
                self.logger.log(f"Method: {method_name}", "SUCCESS")
                self.logger.log(f"Key: {key_used}", "SUCCESS")
                return True, decrypted, key_used, method_name
        
        self.logger.log("\n❌ All initial methods exhausted - Running unlimited Brute Force...", "FAILED")
        return False, "", "", ""


def main():
    """Main entry point."""
    print("\n" + "=" * 80)
    print("null-Encrypter AI-Powered Decryption Tool")
    print("MODE: UNLIMITED (Will run until key is found)")
    print(f"CPU Cores for Parallel Brute Force: {multiprocessing.cpu_count()}") 
    print("=" * 80 + "\n")
    
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <encrypted_text>")
        print()
        print("Example:")
        print(f"  {sys.argv[0]} 'ÑISesA10__ENU4_3LLG26_xHdZ9f20...'")
        print()
        sys.exit(1)
    
    encrypted_text = sys.argv[1]
    
    # Initialize logger
    log_file = f"decryption_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    logger = DecryptionLogger(log_file)
    
    # Initialize AI decryptor
    ai = AIDecryptor(encrypted_text, logger)
    
    # Run all methods
    success, decrypted, key_used, method_used = ai.run_all_methods()
    
    # Finalize log
    logger.finalize(success, key_used, method_used)
    
    # Print results
    print("\n" + "=" * 80)
    if success:
        print("✅ DECRYPTION SUCCESSFUL!")
        print("=" * 80)
        print(f"\nMethod Used: {method_used}")
        print(f"Key: {key_used}")
        print(f"\nDecrypted Text:")
        print("-" * 80)
        print(decrypted)
        print("-" * 80)
    else:
        print("❌ DECRYPTION INITIALLY FAILED - CHECK LOG FOR UNLIMITED BRUTE FORCE PROGRESS")
        print("=" * 80)
    
    elapsed = time.time() - logger.start_time
    print(f"\nTime Elapsed: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
    print(f"Total Attempts Logged: {logger.attempts}")
    print(f"Log File: {log_file}")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
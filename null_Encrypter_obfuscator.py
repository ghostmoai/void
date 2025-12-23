import os
import base64
import shutil
from pathlib import Path

# Configuration
SOURCE_DIR = Path(".")
OUTPUT_DIR = Path("obfuscated_src")

# Files to obfuscate (Python source files)
FILES_TO_OBFUSCATE = [
    "null_Encrypter_core.py",
    "null_Encrypter_encryption.py",
    "null_Encrypter_main.py"
]

FILES_TO_COPY = ["buildozer.spec", "version_info.txt"]
EXTENSIONS_TO_COPY = [".png", ".jpg", ".kv", ".atlas", ".txt", ".key", ".ico"]

def obfuscate_file(file_path, output_path):
    """Obfuscates a python file using base64 encoding and exec wrapper."""
    print(f"Obfuscating {file_path} -> {output_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Simple obfuscation: Base64 encode and wrap in exec
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        obfuscated_code = f"import base64;exec(base64.b64decode('{encoded_content}'))"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(obfuscated_code)
            
    except Exception as e:
        print(f"Error obfuscating {file_path}: {e}")

def main():
    # Create output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    
    # Process files
    for item in SOURCE_DIR.iterdir():
        if item.name in FILES_TO_OBFUSCATE:
            obfuscate_file(item, OUTPUT_DIR / item.name)
        elif item.name in FILES_TO_COPY or item.suffix in EXTENSIONS_TO_COPY:
            if item.is_file():
                shutil.copy2(item, OUTPUT_DIR / item.name)
                print(f"Copied {item.name}")
            elif item.is_dir() and item.name not in [".buildozer", ".venv", "venv", "__pycache__", "bin", "dist", "obfuscated_src"]:
                 # Copy directories recursively if needed, but be careful with exclusions
                 # For now, let's just copy specific files or assets folders if known
                 pass

    print(f"\nObfuscation complete. Files are in '{OUTPUT_DIR}'.")
    print("Update buildozer.spec to set 'source.dir = obfuscated_src'")

if __name__ == "__main__":
    main()

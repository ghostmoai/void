#!/bin/bash
# Script de compilación para null-Encrypter PC
# Crea un ejecutable standalone usando PyInstaller

echo "🔨 Compilando null-Encrypter para PC..."
echo ""

# Verificar PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip3 install --user pyinstaller
fi

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/ *.spec

# Compilar main.py (GUI)
echo "🔨 Compilando versión GUI..."
pyinstaller --onefile \
    --name "null-Encrypter" \
    --add-data "null_Encrypter_encryption.py:." \
    --hidden-import kivy \
    --hidden-import plyer \
    --noconsole \
    main.py

# Compilar encrypt_pc.py (CLI)
echo "🔨 Compilando versión CLI..."
pyinstaller --onefile \
    --name "null-encrypter-cli" \
    --add-data "null_Encrypter_encryption.py:." \
    encrypt_pc.py

echo ""
echo "✅ Compilación completada!"
echo ""
echo "📁 Ejecutables generados:"
echo "   - dist/null-Encrypter (GUI)"
echo "   - dist/null-encrypter-cli (CLI)"
echo ""
echo "💡 Uso:"
echo "   GUI: ./dist/null-Encrypter"
echo "   CLI: ./dist/null-encrypter-cli encrypt archivo.pdf"

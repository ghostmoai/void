# 🖥️ Compilación para PC - null-Encrypter

## Opciones de Uso en PC

### Opción 1: Ejecutar directamente con Python (Recomendado)

No requiere compilación, solo Python 3.8+:

```bash
# CLI (Línea de comandos)
python3 encrypt_pc.py encrypt archivo.pdf
python3 encrypt_pc.py decrypt archivo.pdf.enc

# GUI (Interfaz gráfica)
python3 main.py
```

### Opción 2: Compilar ejecutable standalone

Si quieres crear un ejecutable que no requiera Python instalado:

#### Requisitos
```bash
pip3 install --user pyinstaller
```

#### Compilar
```bash
chmod +x build_pc.sh
./build_pc.sh
```

Esto generará:
- `dist/null-Encrypter` - Versión GUI
- `dist/null-encrypter-cli` - Versión CLI

#### Uso de ejecutables
```bash
# CLI
./dist/null-encrypter-cli encrypt documento.pdf
./dist/null-encrypter-cli decrypt documento.pdf.enc

# GUI
./dist/null-Encrypter
```

## 📦 Distribución

### Crear paquete portable

```bash
# Copiar ejecutables y dependencias
mkdir null-encrypter-portable
cp dist/null-encrypter-cli null-encrypter-portable/
cp README.md null-encrypter-portable/
cp CHANGELOG.md null-encrypter-portable/

# Crear archivo tar.gz
tar -czf null-encrypter-v2.0.0-linux.tar.gz null-encrypter-portable/
```

## 🐧 Linux

### Instalación del CLI en el sistema

```bash
# Copiar a /usr/local/bin
sudo cp dist/null-encrypter-cli /usr/local/bin/null-encrypter
sudo chmod +x /usr/local/bin/null-encrypter

# Ahora puedes usar desde cualquier lugar
null-encrypter encrypt archivo.pdf
```

## 🪟 Windows

Para Windows, usa el script de Python directamente o compila con PyInstaller en Windows:

```powershell
# Instalar PyInstaller
pip install pyinstaller

# Compilar
pyinstaller --onefile --name null-encrypter-cli encrypt_pc.py

# Ejecutar
.\dist\null-encrypter-cli.exe encrypt archivo.pdf
```

## 💡 Recomendación

Para la mayoría de usuarios, **usar directamente con Python** es la mejor opción:
- ✅ Más simple
- ✅ Más rápido
- ✅ Fácil de actualizar
- ✅ No requiere compilación

Solo compila si necesitas distribuir a usuarios sin Python instalado.

---

**Nota:** El ejecutable compilado será más grande (~10-20 MB) porque incluye el intérprete de Python.

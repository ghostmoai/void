# 🔐 null-Encrypter v2.0.0

**Encriptación segura y portable entre PC y Android**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/eltionull/null-encrypter)
[![Platform](https://img.shields.io/badge/platform-Android%2011%2B-green.svg)](https://www.android.com/)
[![License](https://img.shields.io/badge/license-Custom-orange.svg)](Licencia%20Pública%20–%20EncryptorX.txt)

---

## 📋 Índice

- [Características](#-características)
- [Instalación](#-instalación)
- [Uso en PC](#-uso-en-pc)
- [Uso en Android](#-uso-en-android)
- [Portabilidad](#-portabilidad-pc--android)
- [Changelog](#-changelog)
- [Seguridad](#-seguridad)
- [Compilación](#-compilación)

---

## ✨ Características

### v2.0.0 - Portabilidad Completa

- 🔄 **Portabilidad PC ↔️ Android**: Archivos encriptados funcionan en cualquier dispositivo
- 📁 **Carpeta `null-txt`**: Organización automática de textos encriptados
- 💾 **Botón Save**: Guarda texto encriptado con timestamp
- 💻 **Script CLI**: Herramienta de línea de comandos para PC
- 🔐 **Seguridad**: Cifrado de flujo con SHA-256, clave de 256 bits, nonce aleatorio
- 🎨 **Ofuscación**: Patrones característicos "Null" para máxima seguridad

---

## 📥 Instalación

### Android

1. Descarga el APK desde [Releases](https://github.com/eltionull/null-encrypter/releases)
2. Instala en tu dispositivo Android 11+
3. Abre la app y comienza a encriptar

### PC (Linux/WSL)

```bash
git clone https://github.com/eltionull/null-encrypter.git
cd null-encrypter
python3 -m pip install -r requirements.txt
```

---

## 💻 Uso en PC

### Script CLI

#### Encriptar Archivos
```bash
python3 encrypt_pc.py encrypt documento.pdf
# Genera: documento.pdf.enc
```

#### Desencriptar Archivos
```bash
python3 encrypt_pc.py decrypt documento.pdf.enc
# Restaura: documento.pdf
```

#### Encriptar Texto
```bash
python3 encrypt_pc.py encrypt-text "Mensaje secreto"
# Guarda en: null-txt/encrypted_text.txt
```

#### Desencriptar Texto
```bash
python3 encrypt_pc.py decrypt-text "Ñn0_Mllu..."
```

### Interfaz Gráfica (Kivy)

```bash
python3 main.py
```

---

## 📱 Uso en Android

### Encriptar Texto
1. Escribe o pega tu mensaje en "Input Message"
2. Toca "🔒 Encrypt"
3. El resultado aparece en "Output Result"
4. Usa "💾 Save" para guardar en archivo
5. O "📋 Copy" para copiar al portapapeles

### Encriptar Archivos
1. Toca "📁 Encrypt File"
2. Selecciona el archivo
3. Elige ubicación para guardar `.enc`
4. ¡Listo! Archivo encriptado

### Desencriptar
1. Toca "📂 Decrypt File"
2. Selecciona archivo `.enc`
3. Elige ubicación para guardar
4. Archivo desencriptado

---

## 🌍 Portabilidad PC ↔️ Android

### Flujo PC → Android

```
┌─────────────────────────────────────────┐
│ 1. PC: Encriptar                        │
│    $ python3 encrypt_pc.py encrypt      │
│      foto.jpg                           │
│    ✅ foto.jpg.enc creado               │
│                                         │
│ 2. Transferir archivo                   │
│    USB / Email / Cloud                  │
│                                         │
│ 3. Android: Desencriptar                │
│    App → Decrypt File → foto.jpg.enc    │
│    ✅ foto.jpg restaurado               │
└─────────────────────────────────────────┘
```

**✨ Sin necesidad de transferir claves** - La clave está embebida de forma segura en el archivo

---

## 📜 Changelog

### v2.0.0 (2025-12-03)

#### ✨ Nuevas Funcionalidades
- **Portabilidad completa**: Clave embebida en archivos
- **Carpeta null-txt**: `Downloads/null-txt/` para textos
- **Botón Save**: Guarda con timestamp automático
- **Script CLI**: `encrypt_pc.py` para terminal

#### 🐛 Correcciones
- Bug de crash al iniciar (v1.0)
- Archivos sincronizados en `obfuscated_src/`

#### 🔧 Cambios Técnicos
- Nuevas funciones: `_embed_key_string()`, `_extract_key_from_string()`
- Formato: `NULL_ENC_HEADER:[clave]:END_HEADER:[datos]`
- Retrocompatible con v1.0

### v1.0.0 (2025-11-XX)
- Lanzamiento inicial
- Encriptación de texto y archivos
- Sistema de logs
- UI con Kivy

---

## 🔐 Seguridad

### Algoritmo de Encriptación

```python
# Stream Cipher personalizado
Keystream = SHA256(Key + Nonce + Counter)
Encrypted = Data XOR Keystream
```

### Características de Seguridad

| Característica | Especificación |
|---|---|
| Algoritmo | Stream Cipher (XOR + SHA256) |
| Tamaño de Clave | 256 bits (32 bytes) |
| Nonce | 128 bits aleatorio |
| Ofuscación | Patrones característicos "Null" |
| Portabilidad | Clave embebida con ofuscación |

### Formato de Archivo Encriptado

```
┌──────────────────────────────────────┐
│ NULL_ENC_HEADER:                     │
│ n0_Mllu37_5LNr41_Uoln36_vul...      │
│ :END_HEADER:                         │
├──────────────────────────────────────┤
│ [Nonce 16 bytes]                     │
│ [Datos encriptados]                  │
└──────────────────────────────────────┘
```

---

## 🛠️ Compilación

### Requisitos
- Python 3.8+
- Buildozer
- Android SDK/NDK

### Compilar APK

#### Debug
```bash
cd ~/EncryptorApp
buildozer android debug
```

#### Release
```bash
buildozer android release
```

### Instalar APK
```bash
adb install bin/nullencrypter-2.0.0-debug.apk
```

---

## 📁 Estructura del Proyecto

```
EncryptorApp/
├── main.py                      # App principal (Kivy)
├── null_Encrypter_encryption.py # Lógica de encriptación
├── encrypt_pc.py                # Script CLI
├── test_encryption.py           # Tests
├── buildozer.spec               # Configuración Android
├── README.md                    # Este archivo
├── CHANGELOG.md                 # Historial detallado
└── obfuscated_src/              # Archivos para build
    ├── main.py
    └── null_Encrypter_encryption.py
```

---

## 🧪 Tests

```bash
python3 test_encryption.py
```

**Resultados esperados:**
```
✅ Test 1: Text Encryption/Decryption
✅ Test 2: File Encryption (Embedded Key)
✅ Test 3: Portability Simulation
✅ Test 4: null-txt Folder Creation
```

---

## 🎯 Roadmap

### v2.1 (Planificado)
- [ ] Compartir archivos directamente
- [ ] Integración con servicios cloud
- [ ] Modo oscuro/claro
- [ ] Historial de archivos

### v3.0 (Futuro)
- [ ] Encriptación de carpetas
- [ ] Compartir con múltiples usuarios
- [ ] Gestión avanzada de claves
- [ ] Sincronización multi-dispositivo

---

## 👤 Autor

**el_tio_null**  
📧 Email: encryternull@gmail.com  
🌐 GitHub: [@eltionull](https://github.com/eltionull)

---

## 📄 Licencia

Ver [Licencia Pública – EncryptorX.txt](Licencia%20Pública%20–%20EncryptorX.txt)

---

## 🙏 Agradecimientos

Gracias a todos los que han contribuido y probado null-Encrypter.

---

**Última actualización:** 2025-12-03  
**Versión:** 2.0.0  
**Plataformas:** Android 11+, Linux, Windows

# 📜 CHANGELOG - null-Encrypter

## Historial de Versiones y Actualizaciones

---

## 🚀 v2.0.0.2 - "Estabilidad Windows" (2025-12-03)

### 🔧 Correcciones y Mejoras
- **[FIX]** Solucionado error `ModuleNotFoundError: kivy` mediante instalación robusta de dependencias (`kivy[base]`, `sdl2`, `glew`).
- **[FIX]** Nuevo sistema de compilación con entorno virtual aislado (`venv`) para evitar conflictos.
- **[FEAT]** Ruta de datos establecida en `C:\null\EncryptorApp` para Windows, asegurando persistencia y organización.
- **[SYS]** Implementación de sistema de versionado automático (ciclo de 5 cambios).

---

## 🚀 v2.0.0.1 - "Paridad UI PC" (2025-12-03)

### ✨ Novedades
- **🖥️ UI de PC idéntica a Android**: Ahora el ejecutable de Windows incluye la interfaz gráfica completa (Kivy).
- **🔢 Versión unificada**: Misma experiencia visual y funcional en todas las plataformas.

---

## 🚀 v2.0.0 - "Portabilidad Completa" (2025-12-03)

### 🎯 Objetivo Principal
Implementar portabilidad total entre PC y Android mediante claves embebidas en archivos encriptados.

### ✨ Nuevas Funcionalidades

#### 1. **Portabilidad PC ↔️ Android**
```
┌─────────────────────────────────────────────────────────┐
│  PC                        Android                      │
│  ┌──────────┐             ┌──────────┐                 │
│  │ Encrypt  │────────────▶│ Decrypt  │                 │
│  │ File     │  .enc file  │ File     │                 │
│  └──────────┘             └──────────┘                 │
│       ▲                         │                       │
│       │      Embedded Key       │                       │
│       └─────────────────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

**Características:**
- ✅ Clave embebida en header del archivo
- ✅ Patrones de ofuscación característicos
- ✅ No requiere transferir `key.key`
- ✅ Retrocompatible con v1.0

**Formato de Archivo:**
```
NULL_ENC_HEADER:[n0_Mllu37_5LNr...]:END_HEADER:[datos_encriptados]
```

#### 2. **Carpeta `null-txt`**
```
Downloads/
└── null-txt/
    ├── encrypted_text_20251203_182030.txt
    ├── encrypted_text_20251203_182145.txt
    └── encrypted_text_20251203_182301.txt
```

**Características:**
- 📁 Carpeta dedicada para textos encriptados
- 🕒 Nombres con timestamp automático
- 📱 Ubicación: `Downloads/null-txt/` (Android)
- 💻 Ubicación: `~/EncryptorApp/null-txt/` (PC)

#### 3. **Botón "Save" en UI**

**Antes (v1.0):**
```
┌─────────────────────────────────────────┐
│ Output Result                           │
│ ┌─────┐ ┌───────┐                      │
│ │ 📋  │ │  🗑️   │                      │
│ │Copy │ │ Clear │                      │
│ └─────┘ └───────┘                      │
└─────────────────────────────────────────┘
```

**Ahora (v2.0):**
```
┌─────────────────────────────────────────┐
│ Output Result                           │
│ ┌─────┐ ┌──────┐ ┌───────┐            │
│ │ 📋  │ │  💾  │ │  🗑️   │            │
│ │Copy │ │ Save │ │ Clear │            │
│ └─────┘ └──────┘ └───────┘            │
└─────────────────────────────────────────┘
```

**Funcionalidad:**
- Guarda texto encriptado en archivo
- Timestamp automático
- Ubicación: carpeta `null-txt`

#### 4. **Script CLI para PC**

**Nuevo archivo:** `encrypt_pc.py`

```bash
# Encriptar archivos
$ python3 encrypt_pc.py encrypt documento.pdf
🔒 Encriptando: documento.pdf
✅ Archivo encriptado exitosamente!
📁 Guardado en: documento.pdf.enc
✅ Header de portabilidad incluido

# Desencriptar archivos
$ python3 encrypt_pc.py decrypt documento.pdf.enc
🔓 Desencriptando: documento.pdf.enc
✅ Archivo desencriptado exitosamente!

# Encriptar texto
$ python3 encrypt_pc.py encrypt-text "Mensaje secreto"
🔒 Encriptando texto...
✅ Texto encriptado
💾 Guardado en: null-txt/encrypted_text.txt
```

### 🐛 Correcciones de Bugs

#### Bug de Crash al Iniciar (v1.0)
**Síntoma:**
```
┌─────────────────────┐
│                     │
│     Loading...      │
│                     │
└─────────────────────┘
         ↓
┌─────────────────────┐
│                     │
│   App se cierra     │
│                     │
└─────────────────────┘
```

**Causa:**
- Archivos desactualizados en `obfuscated_src/`
- Incompatibilidad entre versiones

**Solución:**
- ✅ Sincronizados `main.py` y `null_Encrypter_encryption.py`
- ✅ Actualizados archivos en `obfuscated_src/`
- ✅ Verificada compatibilidad

### 🔧 Cambios Técnicos

#### `null_Encrypter_encryption.py`

**Nuevas Funciones:**
```python
def _embed_key_string(key_bytes: bytes) -> str:
    """Crea string con clave dispersa usando patrones"""
    # Genera: n0_Mllu37_5LNr41_Uoln36_vul...

def _extract_key_from_string(content: str) -> bytes:
    """Extrae clave de string usando regex de patrones"""
    # Reconstruye la clave original
```

**Función Actualizada:**
```python
def encrypt_file(file_path: str) -> bytes:
    # ANTES (v1.0)
    return _encrypt(file_data, CLAVE)
    
    # AHORA (v2.0)
    key_header_str = _embed_key_string(CLAVE)
    full_header = f"NULL_ENC_HEADER:{key_header_str}:END_HEADER:"
    return full_header.encode('utf-8') + _encrypt(file_data, CLAVE)
```

#### `main.py`

**Nueva Propiedad:**
```python
self.null_txt_path = downloads_path / "null-txt"
self.null_txt_path.mkdir(exist_ok=True)
```

**Nueva Función:**
```python
def save_output_to_file(self, _instance):
    """Guarda output en archivo con timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"encrypted_text_{timestamp}.txt"
    filepath = self.null_txt_path / filename
    # Guarda contenido...
```

**UI Actualizada:**
```python
# Footer
text="v2.0.0 | Secure Encryption"  # Antes: v1.0.0

# Logs de inicio
self.log(f"Encrypted texts folder: {self.null_txt_path}")  # Nuevo
```

### 📊 Comparación de Versiones

| Característica | v1.0 | v2.0 |
|---|:---:|:---:|
| **Funcionalidad** |
| Encriptar texto | ✅ | ✅ |
| Desencriptar texto | ✅ | ✅ |
| Encriptar archivos | ✅ | ✅ |
| Desencriptar archivos | ✅ | ✅ |
| Portabilidad PC↔️Android | ❌ | ✅ |
| Guardar texto en archivo | ❌ | ✅ |
| Script CLI | ❌ | ✅ |
| **UI/UX** |
| Botón Save | ❌ | ✅ |
| Carpeta null-txt | ❌ | ✅ |
| Timestamp en archivos | ❌ | ✅ |
| **Seguridad** |
| Cifrado stream cipher | ✅ | ✅ |
| Nonce aleatorio | ✅ | ✅ |
| Clave 256-bit | ✅ | ✅ |
| Clave embebida | ❌ | ✅ |
| Ofuscación de patrones | ✅ | ✅ |
| **Compatibilidad** |
| Archivos v1.0 | N/A | ✅ |
| Archivos v2.0 | N/A | ✅ |
| **Bugs** |
| Crash al iniciar | 🐛 | ✅ |

### 📦 Archivos Modificados

```diff
obfuscated_src/
+ main.py                      (21 KB) - Actualizado
+ null_Encrypter_encryption.py (14 KB) - Actualizado
  buildozer.spec               (14 KB) - Version 2.0.0

root/
+ main.py                      (21 KB) - Actualizado
+ null_Encrypter_encryption.py (14 KB) - Actualizado
+ encrypt_pc.py                (4 KB)  - Nuevo
+ test_encryption.py           (2 KB)  - Actualizado
+ GUIA_USO_PC.md              (5 KB)  - Nuevo
+ RELEASE_NOTES_v2.0.0.md     (6 KB)  - Nuevo
+ CHANGELOG.md                (Este archivo) - Nuevo
```

### 🧪 Tests Ejecutados

```
┌─────────────────────────────────────────────────────┐
│ Test Suite v2.0                                     │
├─────────────────────────────────────────────────────┤
│ ✅ Test 1: Text Encryption/Decryption              │
│    Encrypted Length: 1234 chars                     │
│    Status: SUCCESS                                  │
│                                                     │
│ ✅ Test 2: File Encryption (Embedded Key)          │
│    File Size: 599 bytes                            │
│    Header Found: YES                               │
│    Status: SUCCESS                                  │
│                                                     │
│ ✅ Test 3: Portability Simulation                  │
│    Different Key: 5a0fe434f1f84a9a...              │
│    Decryption: SUCCESS                             │
│    Status: VERIFIED                                 │
│                                                     │
│ ✅ Test 4: null-txt Folder Creation                │
│    Location: ~/EncryptorApp/null-txt/              │
│    File Created: encrypted_text.txt                │
│    Status: SUCCESS                                  │
└─────────────────────────────────────────────────────┘
```

---

## 📝 v1.0.0 - "Lanzamiento Inicial" (2025-11-XX)

### ✨ Funcionalidades Iniciales

#### 1. **Encriptación de Texto**
```
┌─────────────────────────────────────────┐
│ Input Message                           │
│ ┌─────────────────────────────────────┐ │
│ │ Hola mundo                          │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────┐ ┌──────────┐              │
│ │🔒Encrypt│ │🔓Decrypt │              │
│ └─────────┘ └──────────┘              │
│                                         │
│ Output Result                           │
│ ┌─────────────────────────────────────┐ │
│ │ Ñn0_Mllu37_5LNr41_Uoln36_vul...    │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Características:**
- Encriptación con patrones de ofuscación
- Clave embebida en texto (no en archivos)
- Copiar/pegar desde clipboard

#### 2. **Encriptación de Archivos**
```
┌─────────────────────────────────────────┐
│ File Operations                         │
│ ┌──────────────┐ ┌──────────────┐     │
│ │📁 Encrypt    │ │📂 Decrypt    │     │
│ │   File       │ │   File       │     │
│ └──────────────┘ └──────────────┘     │
└─────────────────────────────────────────┘
```

**Características:**
- Selección de archivos con plyer
- Extensión `.enc` automática
- Límite de 500 MB

#### 3. **Sistema de Logs**
```
┌─────────────────────────────────────────┐
│ System Log                              │
│ ┌─────────────────────────────────────┐ │
│ │ [System Ready] initialized          │ │
│ │ [2025-11-XX 10:30:00] Key loaded    │ │
│ │ [2025-11-XX 10:30:05] Text encrypted│ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Características:**
- Logs en tiempo real
- Guardado en archivo
- Timestamps automáticos

### 🔒 Seguridad v1.0

```
┌─────────────────────────────────────────┐
│ Security Features                       │
├─────────────────────────────────────────┤
│ • Stream Cipher (XOR + SHA256)          │
│ • 256-bit Key                           │
│ • 128-bit Random Nonce                  │
│ • Obfuscation Patterns                  │
│ • Local Key Storage                     │
└─────────────────────────────────────────┘
```

### ⚠️ Limitaciones v1.0

```
┌─────────────────────────────────────────┐
│ Known Limitations                       │
├─────────────────────────────────────────┤
│ ❌ No portabilidad de archivos          │
│ ❌ Requiere misma clave en todos los    │
│    dispositivos                         │
│ ❌ No hay carpeta dedicada para textos  │
│ ❌ No hay script CLI                    │
│ 🐛 Crash al iniciar en algunos casos   │
└─────────────────────────────────────────┘
```

---

## 🎯 Roadmap Futuro

### v2.1 (Planificado)
```
┌─────────────────────────────────────────┐
│ Planned Features                        │
├─────────────────────────────────────────┤
│ 📤 Compartir archivos directamente      │
│ ☁️  Integración con servicios cloud     │
│ 🌓 Modo oscuro/claro                    │
│ 📋 Historial de archivos encriptados   │
│ 🔍 Búsqueda en archivos encriptados    │
└─────────────────────────────────────────┘
```

### v3.0 (Futuro)
```
┌─────────────────────────────────────────┐
│ Future Vision                           │
├─────────────────────────────────────────┤
│ 🔐 Encriptación de carpetas completas   │
│ 👥 Compartir con múltiples usuarios     │
│ 🔑 Gestión avanzada de claves          │
│ 📊 Estadísticas de uso                 │
│ 🌐 Sincronización multi-dispositivo    │
└─────────────────────────────────────────┘
```

---

## 📈 Evolución del Proyecto

```
Timeline:
─────────────────────────────────────────────────────────────
2025-11-XX          2025-12-03          Futuro
    │                   │                  │
    v                   v                  v
  v1.0.0              v2.0.0             v2.1+
    │                   │                  │
    │                   │                  │
┌───┴────┐         ┌────┴─────┐      ┌────┴─────┐
│ Basic  │────────▶│Portable  │─────▶│ Cloud    │
│Encrypt │         │+ CLI     │      │+ Share   │
└────────┘         └──────────┘      └──────────┘

Features Added:
v1.0: ████░░░░░░ 40%
v2.0: ████████░░ 80%
v2.1: ██████████ 100% (planned)
```

---

## 👤 Información del Proyecto

**Autor:** el_tio_null  
**Email:** encryternull@gmail.com  
**Licencia:** Ver `Licencia Pública – EncryptorX.txt`  
**Plataformas:** Android 11+ (API 30+), Linux, Windows  

---

## 📚 Documentación Adicional

- `GUIA_USO_PC.md` - Guía completa de uso en PC
- `RELEASE_NOTES_v2.0.0.md` - Notas detalladas de v2.0
- `README.md` - Información general del proyecto
- `walkthrough.md` - Documentación técnica de implementación

---

**Última actualización:** 2025-12-03  
**Versión actual:** 2.0.0

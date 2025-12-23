# AI-Powered Brute Force Decryption Tool

## fuerza.py - Herramienta de Descifrado con IA

Herramienta avanzada que utiliza múltiples métodos inteligentes para descifrar mensajes encriptados con null-Encrypter.

### 🤖 Características de IA

La herramienta prueba automáticamente 6 métodos diferentes en secuencia:

1. **Extracción de Clave Embebida** - Intenta extraer la clave del mensaje
2. **Clave por Defecto** - Prueba con la clave del sistema
3. **Base de Datos de Claves Comunes** - Prueba claves conocidas
4. **Análisis de Patrones** - Analiza la estructura del mensaje
5. **Ataque de Diccionario** - Prueba palabras comunes y variaciones
6. **Fuerza Bruta Limitada** - Prueba combinaciones aleatorias

### 📊 Sistema de Logging

Cada ejecución genera un log detallado con:
- ⏱️ Timestamp de cada intento
- 🔑 Clave probada
- ✅/❌ Resultado (éxito/fallo)
- 📈 Progreso en tiempo real
- 📝 Resumen final con estadísticas

### 🚀 Uso

```bash
python3 fuerza.py "texto_encriptado"
```

### 📄 Ejemplo de Log

El archivo de log incluye:
```
================================================================================
null-Encrypter AI Decryption Log
Started: 2025-12-02 15:00:00
================================================================================

[    0.00s] [START  ] Starting AI-powered decryption process...
[    0.01s] [INFO   ] Encrypted text length: 933 characters
[    0.01s] [METHOD ] ============================================================
[    0.01s] [METHOD ] Starting Method: Embedded Key Extraction
[    0.02s] [SUCCESS] Attempt #1 | Method: Embedded Key | Key: Extracted from message | ✅ SUCCESS
[    0.02s] [RESULT ] Decrypted text: Hola mundo! 123

================================================================================
DECRYPTION SUMMARY
================================================================================
Status: SUCCESS ✅
Total Attempts: 1
Methods Tried: 1
Time Elapsed: 0.02 seconds (0.00 minutes)
Successful Method: Embedded Key Extraction
Key Used: Extracted from message
```

### ⚙️ Configuración

Puedes ajustar los límites en el código:
- `max_words` en `method_5_dictionary_attack()` - Número de palabras a probar
- `max_attempts` en `method_6_brute_force_short()` - Intentos de fuerza bruta

### 📈 Estadísticas

La herramienta registra:
- Número total de intentos
- Tiempo transcurrido
- Método exitoso (si aplica)
- Clave utilizada
- Lista de todos los métodos probados

### ⚠️ Nota Legal

Esta herramienta es solo para propósitos educativos y de recuperación de datos propios.

# spec-gen

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

CLI en Python que genera archivos de especificación SDD (REQUIREMENTS.md, DESIGN.md, TASKS.md)
desde una idea en lenguaje natural, usando LLMs.

## Características

- Genera 3 archivos de especificación: REQUIREMENTS.md, DESIGN.md, TASKS.md
- Soporta múltiples providers: Groq, Qwen, OpenAI-compatible
- Preview de archivos generados en la terminal
- Interface intuitiva con colores y spinners

## Requisitos

- Python 3.11 o superior
- Una API key de Groq, Qwen u otro provider compatible con OpenAI

## Instalación

### Desde GitHub

```bash
pip install git+https://github.com/tu-usuario/spec-gen.git
```

### Edición local (desarrollo)

```bash
git clone https://github.com/tu-usuario/spec-gen.git
cd spec-gen
pip install -e ".[dev]"
```

## Configuración

### 1. Obtén una API key de Groq

Regístrate en [console.groq.com](https://console.groq.com) y crea una API key.

### 2. Configura la variable de entorno

```bash
# Linux/macOS
export SPEC_GEN_API_KEY=gsk_xxxxx

# Windows (CMD)
set SPEC_GEN_API_KEY=gsk_xxxxx

# Windows (PowerShell)
$env:SPEC_GEN_API_KEY="gsk_xxxxx"
```

### 3. (Opcional) Configura el provider

```bash
spec-gen config
```

Esto guardará la configuración en `~/.spec-gen/config.toml`.

## Uso

### Generar especificaciones

```bash
spec-gen init "una API REST para gestionar inspecciones NDT"
```

Opciones disponibles:
- `--output, -o`: Directorio de salida (default: actual)
- `--lang`: Idioma `es` o `en` (default: `es`)
- `--force, -f`: Sobrescribir sin confirmar
- `--no-preview`: Omitir preview de archivos

### Regenerar un archivo específico

```bash
spec-gen regen --file requirements
spec-gen regen --file design
spec-gen regen --file tasks
```

### Ver archivos generados

```bash
spec-gen show --file requirements
spec-gen show --file all
```

### Ver configuración

```bash
spec-gen config --show
```

## Ejemplo completo

```bash
# 1. Instalar
pip install git+https://github.com/tu-usuario/spec-gen.git

# 2. Configurar API key
export SPEC_GEN_API_KEY=gsk_xxxxx

# 3. Generar especificaciones
spec-gen init "un sistema de inventario para una ferretería"

# 4. Ver el resultado
ls -la
# REQUIREMENTS.md
# DESIGN.md
# TASKS.md

# 5. Regenerar si necesitas cambios
spec-gen regen --file tasks
```

## Estructura de archivos generados

### REQUIREMENTS.md
Descripción del producto, casos de uso, requisitos no funcionales y modelo de datos.

### DESIGN.md
Arquitectura del sistema, ADRs, estructura de carpetas, APIs y dependencias.

### TASKS.md
Lista de tareas atómicas organizadas por fases, ordenadas por dependencia.

## Providers soportados

| Provider | Base URL | Modelos sugeridos |
|----------|----------|-------------------|
| Groq | `https://api.groq.com/openai/v1` | llama-3.3-70b-versatile |
| Qwen | `https://dashscope.aliyuncs.com/compatible-mode/v1` | qwen-plus |
| OpenCode | Configurable | cualquiera compatible con OpenAI |

## Desarrollo

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/spec-gen.git
cd spec-gen

# Instalar con dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar tests
pytest tests/ -v

# Linting
ruff check .
ruff format .
```

## Licencia

MIT License

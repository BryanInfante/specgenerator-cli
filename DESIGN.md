# DESIGN.md
# AI Spec Generator CLI — spec-gen

## 1. Arquitectura general

```
spec-gen/
├── spec_gen/
│   ├── __init__.py
│   ├── cli.py            # Entrypoint Click — comandos init, regen, config, show
│   ├── config.py         # Lectura/escritura de ~/.spec-gen/config.toml
│   ├── generator.py      # Lógica de generación — llama al provider
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py       # Clase abstracta BaseProvider
│   │   ├── qwen.py       # Implementación Qwen (DashScope)
│   │   └── opencode.py   # Implementación Open Code
│   ├── prompts/
│   │   ├── requirements.md   # Prompt template para REQUIREMENTS.md
│   │   ├── design.md         # Prompt template para DESIGN.md
│   │   └── tasks.md          # Prompt template para TASKS.md
│   └── renderer.py       # Rich — output en terminal, spinners, colores
├── tests/
│   ├── test_config.py
│   ├── test_generator.py
│   └── test_providers.py
├── pyproject.toml
├── AGENTS.md             # Contexto para agentes IA que trabajen este repo
├── REQUIREMENTS.md       # Este proyecto
├── DESIGN.md
└── TASKS.md
```

---

## 2. Decisiones de arquitectura

### ADR-01: Provider pattern para LLMs
**Decisión:** Cada provider implementa `BaseProvider` con método `complete(prompt: str) -> str`.  
**Razón:** Permite agregar Claude, Gemini u otros en v2.0 sin tocar `generator.py`.  
**Consecuencia:** Pequeño overhead de abstracción que vale la pena desde el inicio.

### ADR-02: Prompts como archivos Markdown, no strings en código
**Decisión:** Los prompts viven en `spec_gen/prompts/*.md`.  
**Razón:** Son editables sin tocar código Python. La comunidad puede hacer PR solo con mejoras de prompts.  
**Consecuencia:** Hay que leerlos desde disco en runtime (costo mínimo).

### ADR-03: Configuración en TOML, no JSON ni .env
**Decisión:** `~/.spec-gen/config.toml` con `tomllib` (stdlib desde Python 3.11).  
**Razón:** TOML es legible, tiene tipos nativos y no requiere dependencia externa.  
**Consecuencia:** No compatible con Python < 3.11 (aceptable, en RNF-02).

### ADR-04: httpx en vez de requests
**Decisión:** Usar `httpx` para llamadas HTTP.  
**Razón:** Async-ready para v2.0, interfaz más moderna, soporta HTTP/2.  
**Consecuencia:** Una dependencia más, pero reemplaza requests que ya conoce la comunidad.

---

## 3. Flujo de generación

```
CLI init "idea"
    │
    ▼
config.py → leer ~/.spec-gen/config.toml
    │
    ▼
generator.py → build_context(idea)
    │
    ├─→ providers/qwen.py → POST /chat/completions
    │         prompt: prompts/requirements.md + idea
    │         → REQUIREMENTS.md
    │
    ├─→ providers/qwen.py → POST /chat/completions
    │         prompt: prompts/design.md + idea + REQUIREMENTS.md
    │         → DESIGN.md
    │
    └─→ providers/qwen.py → POST /chat/completions
              prompt: prompts/tasks.md + idea + REQUIREMENTS.md + DESIGN.md
              → TASKS.md
```

**Nota:** Las 3 llamadas son secuenciales, no paralelas. DESIGN necesita REQUIREMENTS como contexto, TASKS necesita ambos.

---

## 4. Interfaz de comandos

```bash
# Generar spec completa
spec-gen init "descripción de la idea"
spec-gen init "descripción" --output ./mi-proyecto
spec-gen init "descripción" --lang en   # inglés (default: es)

# Regenerar un archivo
spec-gen regen --file requirements
spec-gen regen --file design
spec-gen regen --file tasks
spec-gen regen --file tasks --force     # sin confirmación

# Configuración
spec-gen config                          # wizard interactivo
spec-gen config --show                   # ver config actual (sin API key)

# Ver archivos
spec-gen show --file requirements
spec-gen show --file all
```

---

## 5. Modelo de configuración

```toml
# ~/.spec-gen/config.toml

[provider]
name = "qwen"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model = "qwen-plus"

[output]
language = "es"
overwrite = false
```

La API key se lee **siempre** desde variable de entorno `SPEC_GEN_API_KEY`.  
Nunca se escribe en el archivo de configuración.

---

## 6. Estructura de prompts

Cada prompt template tiene 3 secciones:

```markdown
# [ROLE]
Eres un arquitecto de software experto en Spec-Driven Development...

# [CONTEXT]
{{idea}}
{{existing_requirements}}   ← solo en design.md y tasks.md
{{existing_design}}         ← solo en tasks.md

# [OUTPUT]
Genera SOLO el contenido del archivo, sin explicaciones adicionales.
El archivo debe seguir exactamente esta estructura:
...estructura esperada...
```

---

## 7. Dependencias

```toml
[project]
requires-python = ">=3.11"
dependencies = [
    "click>=8.1",
    "httpx>=0.27",
    "rich>=13.0",
]
```

Sin más dependencias. `tomllib` es stdlib en Python 3.11+.

---

## 8. Entradas/Salidas esperadas

**Input:**
```bash
spec-gen init "quiero un sistema de notificaciones por email para una plataforma SaaS"
```

**Output — 3 archivos generados:**
- `REQUIREMENTS.md` — casos de uso, criterios de aceptación, RNFs
- `DESIGN.md` — arquitectura, ADRs, estructura de carpetas, dependencias
- `TASKS.md` — lista de tareas atómicas con checkboxes, ordenadas por dependencia

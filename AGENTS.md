# AGENTS.md
# spec-gen — Contexto para agentes IA

## ¿Qué es este proyecto?
CLI en Python que genera archivos de especificación SDD (REQUIREMENTS.md, DESIGN.md, TASKS.md)
desde una idea en lenguaje natural, usando LLMs via API compatible con OpenAI.

## Stack
- **Lenguaje:** Python 3.11+
- **CLI:** Click 8.1+
- **HTTP:** httpx (no requests)
- **Terminal UI:** Rich
- **Config:** tomllib (stdlib) + TOML
- **Tests:** pytest
- **Linter:** ruff
- **Empaquetado:** pyproject.toml (no setup.py)

## Estructura de carpetas
```
spec_gen/
├── cli.py          # Comandos Click: init, regen, config, show
├── config.py       # Lectura/escritura ~/.spec-gen/config.toml
├── generator.py    # Orquesta las llamadas al provider
├── renderer.py     # Output en terminal con Rich
└── providers/
    ├── base.py     # Clase abstracta BaseProvider
    ├── qwen.py     # Provider Qwen/DashScope
    └── opencode.py # Provider Open Code
```

## Convenciones de código
- **Naming:** snake_case para funciones y variables, PascalCase para clases
- **Tipos:** type hints en todas las funciones públicas
- **Docstrings:** solo en funciones públicas, formato Google style
- **Imports:** stdlib → third-party → local, separados por línea en blanco
- **Longitud de línea:** 88 chars (ruff default)

## Convenciones de commits
Usar Conventional Commits:
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `chore:` mantenimiento (deps, config)
- `test:` tests
- `docs:` documentación

## Reglas de desarrollo
1. Leer TASKS.md antes de implementar. Marcar tareas como [~] al empezar, [x] al terminar.
2. No modificar la interfaz de BaseProvider sin actualizar DESIGN.md ADR-01.
3. Los prompts en `spec_gen/prompts/` son archivos Markdown — no strings en código.
4. La API key NUNCA se escribe en disco. Siempre desde variable de entorno `SPEC_GEN_API_KEY`.
5. Cada provider debe manejar sus propios errores HTTP con mensajes en español.

## Variables de entorno
```
SPEC_GEN_API_KEY=sk-...   # API key del provider activo (requerida)
```

## Cómo correr los tests
```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Cómo probar el CLI localmente
```bash
pip install -e .
export SPEC_GEN_API_KEY=tu-api-key
spec-gen config
spec-gen init "una API REST para gestionar tareas"
```

## Contexto de decisiones importantes
- **httpx sobre requests:** async-ready para v2.0, ver ADR-04 en DESIGN.md
- **TOML sobre JSON:** legibilidad y tipos nativos, ver ADR-03 en DESIGN.md
- **Prompts como archivos:** editables sin tocar Python, ver ADR-02 en DESIGN.md
- **Provider pattern:** extensible a Claude/Gemini en v2.0, ver ADR-01 en DESIGN.md

# TASKS.md
# AI Spec Generator CLI — spec-gen

## Leyenda
- [ ] Pendiente
- [~] En progreso
- [x] Completado

---

## FASE 1 — Setup del proyecto

- [x] **T-01** Crear estructura de carpetas según DESIGN.md
  - `spec_gen/`, `spec_gen/providers/`, `spec_gen/prompts/`, `tests/`
- [x] **T-02** Inicializar `pyproject.toml` con dependencias (click, httpx, rich)
  - Entry point: `spec-gen = "spec_gen.cli:main"`
- [x] **T-03** Crear `AGENTS.md` con contexto del proyecto para Kiro/Claude Code
  - Stack, convenciones de naming, reglas de desarrollo
- [x] **T-04** Inicializar repositorio Git
  - `.gitignore` con: `__pycache__/`, `*.pyc`, `.env`, `~/.spec-gen/`
  - Primer commit: `chore: initial project structure`

---

## FASE 2 — Configuración

- [x] **T-05** Implementar `config.py`
  - Función `load_config() -> dict` — lee `~/.spec-gen/config.toml`
  - Función `save_config(config: dict)` — escribe el archivo
  - Función `get_api_key() -> str` — lee `SPEC_GEN_API_KEY` del entorno, error claro si no existe
- [x] **T-06** Implementar comando `spec-gen config` en `cli.py`
  - Wizard interactivo con `click.prompt()`
  - Input de API key oculto con `hide_input=True`
  - Confirmación al final: muestra config guardada (sin API key)
- [x] **T-07** Implementar comando `spec-gen config --show`
  - Muestra config actual con Rich Table
  - API key: solo muestra `sk-****...****` (primeros 3 y últimos 4 chars)
- [x] **T-08** Test: `test_config.py`
  - Test load_config con archivo válido
  - Test load_config sin archivo (debe retornar defaults)
  - Test get_api_key con variable de entorno seteada
  - Test get_api_key sin variable de entorno (debe lanzar excepción clara)

---

## FASE 3 — Providers

- [x] **T-09** Implementar `providers/base.py`
  - Clase abstracta `BaseProvider`
  - Método abstracto `complete(prompt: str) -> str`
  - Método `__init__(api_key: str, model: str, base_url: str)`
- [x] **T-10** Implementar `providers/qwen.py`
  - Hereda de `BaseProvider`
  - POST a `/chat/completions` con `httpx`
  - Manejo de errores HTTP (401, 429, 500) con mensajes claros en español
  - Timeout de 60 segundos
- [x] **T-11** Implementar `providers/opencode.py`
  - Igual que qwen.py pero con `base_url` configurable
  - Mismo contrato de interfaz
- [x] **T-12** Implementar factory en `providers/__init__.py`
  - Función `get_provider(config: dict) -> BaseProvider`
  - Retorna la instancia correcta según `config.provider.name`
- [x] **T-13** Test: `test_providers.py`
  - Test con mock de httpx (sin llamadas reales a la API)
  - Test manejo de error 401 (API key inválida)
  - Test manejo de timeout

---

## FASE 4 — Prompts

- [ ] **T-14** Crear `prompts/requirements.md`
  - Role: arquitecto SDD experto
  - Output esperado: estructura completa de REQUIREMENTS.md
  - Instrucción: solo Markdown, sin explicaciones adicionales
- [ ] **T-15** Crear `prompts/design.md`
  - Igual que requirements pero para DESIGN.md
  - Incluye placeholder `{{requirements_context}}`
- [ ] **T-16** Crear `prompts/tasks.md`
  - Incluye placeholders `{{requirements_context}}` y `{{design_context}}`
  - Instrucción: tareas atómicas, ordenadas por dependencia, con checkboxes

---

## FASE 5 — Generador

- [ ] **T-17** Implementar `generator.py`
  - Función `load_prompt(name: str) -> str` — lee desde `spec_gen/prompts/`
  - Función `render_prompt(template: str, **kwargs) -> str` — reemplaza placeholders
  - Función `generate_spec(idea: str, provider: BaseProvider, lang: str) -> dict`
    - Retorna `{"requirements": str, "design": str, "tasks": str}`
    - Llamadas secuenciales: requirements → design (con requirements) → tasks (con ambos)
- [ ] **T-18** Implementar `renderer.py`
  - Función `print_spinner(message: str)` — context manager con Rich Spinner
  - Función `print_success(files: list[str])` — tabla de archivos generados
  - Función `print_error(message: str)` — error formateado en rojo
  - Función `print_markdown(content: str)` — Markdown con syntax highlighting
- [ ] **T-19** Test: `test_generator.py`
  - Test render_prompt con placeholders
  - Test generate_spec con provider mockeado
  - Test que los 3 archivos se generan con contenido no vacío

---

## FASE 6 — CLI principal

- [ ] **T-20** Implementar comando `spec-gen init` en `cli.py`
  - Argumento: `idea` (string)
  - Opción: `--output PATH` (default: directorio actual)
  - Opción: `--lang [es|en]` (default: es)
  - Opción: `--force` (sobreescribir sin confirmar)
  - Flujo: load config → get provider → generate → write files → print success
- [ ] **T-21** Implementar comando `spec-gen regen`
  - Opción: `--file [requirements|design|tasks]` (requerida)
  - Lee archivos existentes como contexto
  - Pide confirmación antes de sobreescribir (omitir con `--force`)
- [ ] **T-22** Implementar comando `spec-gen show`
  - Opción: `--file [requirements|design|tasks|all]`
  - Imprime con Rich Markdown
- [ ] **T-23** Manejo global de errores en `cli.py`
  - API key no configurada → mensaje claro con instrucciones
  - Archivo no encontrado en regen → mensaje claro
  - Error de red → mensaje con sugerencia de retry

---

## FASE 7 — Empaquetado y distribución

- [ ] **T-24** Verificar que `pip install -e .` funciona limpio
- [ ] **T-25** Crear `README.md`
  - Instalación, configuración, ejemplos de uso
  - Badge de versión y Python version
- [ ] **T-26** Crear GitHub Actions CI (`.github/workflows/ci.yml`)
  - Trigger: push a main y PRs
  - Jobs: lint (ruff) → tests (pytest) → build check
- [ ] **T-27** Publicar en PyPI
  - Workflow de release automático al crear un tag `v*.*.*`

---

## Orden de implementación recomendado

```
T-01 → T-02 → T-03 → T-04   (setup)
T-05 → T-06 → T-07 → T-08   (config — primer comando funcional)
T-09 → T-10 → T-11 → T-12 → T-13  (providers)
T-14 → T-15 → T-16          (prompts)
T-17 → T-18 → T-19          (generador)
T-20 → T-21 → T-22 → T-23  (CLI completo)
T-24 → T-25 → T-26 → T-27  (distribución)
```

**Primera milestone funcional:** T-01 al T-13 — ya puedes llamar a Qwen desde código.  
**Segunda milestone funcional:** T-14 al T-20 — `spec-gen init` funciona end-to-end.

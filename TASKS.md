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
  - Función `get_api_key() -> str` — lee `SPEC_GEN_API_KEY` del entorno
- [x] **T-06** Implementar comando `spec-gen config` en `cli.py`
  - Wizard interactivo con `click.prompt()`
  - Input de API key oculto con `hide_input=True`
- [x] **T-07** Implementar comando `spec-gen config --show`
  - Muestra config actual con Rich Table
  - API key: solo muestra `sk-****...****`
- [x] **T-08** Test: `test_config.py`
  - Test load_config con archivo válido
  - Test load_config sin archivo (debe retornar defaults)
  - Test get_api_key con variable de entorno seteada

---

## FASE 3 — Providers

- [x] **T-09** Implementar `providers/base.py`
  - Clase abstracta `BaseProvider`
  - Método abstracto `complete(prompt: str) -> str`
- [x] **T-10** Implementar `providers/qwen.py`
  - Hereda de `BaseProvider`
  - POST a `/chat/completions` con `httpx`
  - Manejo de errores HTTP con mensajes en español
- [x] **T-11** Implementar `providers/opencode.py`
  - Igual que qwen.py pero con `base_url` configurable
- [x] **T-12** Implementar factory en `providers/__init__.py`
  - Función `get_provider(config: dict) -> BaseProvider`
- [x] **T-13** Test: `test_providers.py`
  - Test con mock de httpx

---

## FASE 4 — Prompts

- [x] **T-14** Crear `prompts/requirements.md`
  - Role: arquitecto SDD experto
- [x] **T-15** Crear `prompts/design.md`
  - Incluye placeholder `{{requirements_context}}`
- [x] **T-16** Crear `prompts/tasks.md`
  - Incluye placeholders `{{requirements_context}}` y `{{design_context}}`

---

## FASE 5 — Generador

- [x] **T-17** Implementar `generator.py`
  - `load_prompt()`, `render_prompt()`, `generate_spec()`
- [x] **T-18** Implementar `renderer.py`
  - `print_spinner()`, `print_success()`, `print_error()`, `print_markdown()`
- [x] **T-19** Test: `test_generator.py`

---

## FASE 6 — CLI principal

- [x] **T-20** Implementar comando `spec-gen init`
  - Argumento: `idea`, opciones: `--output`, `--lang`, `--force`
- [x] **T-21** Implementar comando `spec-gen regen`
  - Opción: `--file [requirements|design|tasks]`
- [x] **T-22** Implementar comando `spec-gen show`
  - Opción: `--file [requirements|design|tasks|all]`
- [x] **T-23** Manejo global de errores en `cli.py`

---

## FASE 7 — Empaquetado y distribución

- [x] **T-24** Verificar que `pip install -e .` funciona limpio
- [x] **T-25** Crear `README.md`
  - Instalación vía GitHub
  - Configuración de API key
  - Ejemplos de uso
- [ ] **T-26** Crear GitHub Actions CI (pendiente)
- [ ] **T-27** Publicar en PyPI (pendiente)

---

## Orden de implementación completado

```
T-01 → T-02 → T-03 → T-04   ✓ (setup)
T-05 → T-06 → T-07 → T-08   ✓ (config)
T-09 → T-10 → T-11 → T-12 → T-13  ✓ (providers)
T-14 → T-15 → T-16          ✓ (prompts)
T-17 → T-18 → T-19          ✓ (generador)
T-20 → T-21 → T-22 → T-23  ✓ (CLI completo)
T-24 → T-25                 ✓ (empaquetado)
```

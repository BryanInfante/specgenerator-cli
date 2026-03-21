# REQUIREMENTS.md
# AI Spec Generator CLI — spec-gen

## 1. Descripción del producto

CLI en Python que recibe una idea en lenguaje natural y genera automáticamente
los archivos de especificación necesarios para Spec-Driven Development:
- `REQUIREMENTS.md`
- `DESIGN.md`
- `TASKS.md`

Pensado para developers que usan Kiro IDE, Claude Code, Qwen Code u Open Code
como agentes de desarrollo.

---

## 2. Usuarios objetivo

- Developers que practican SDD con agentes IA
- Equipos que quieren estandarizar la documentación de proyectos
- Comunidad hispanohablante de desarrollo con IA

---

## 3. Casos de uso

### UC-01 — Generar spec completa desde una idea
**Actor:** Developer  
**Precondición:** Tiene una API key de Qwen configurada  
**Flujo:**
1. Developer ejecuta `spec-gen init "quiero una API REST para gestionar inspecciones NDT"`
2. CLI muestra un spinner mientras llama a la API de Qwen
3. CLI genera los 3 archivos en el directorio actual (o en `--output`)
4. CLI imprime resumen de lo generado

**Criterios de aceptación:**
- Los 3 archivos se generan en menos de 30 segundos
- Cada archivo tiene estructura Markdown válida
- El contenido es coherente entre los 3 archivos (mismo proyecto, mismas entidades)

---

### UC-02 — Regenerar un archivo específico
**Actor:** Developer  
**Flujo:**
1. Developer ejecuta `spec-gen regen --file tasks`
2. CLI lee el REQUIREMENTS.md y DESIGN.md existentes como contexto
3. CLI regenera solo TASKS.md respetando el contexto existente

**Criterios de aceptación:**
- Solo sobreescribe el archivo solicitado
- Pide confirmación antes de sobreescribir (`--force` para omitir)
- Usa el contexto de los otros archivos existentes

---

### UC-03 — Configurar modelo y API key
**Actor:** Developer  
**Flujo:**
1. Developer ejecuta `spec-gen config`
2. CLI solicita: provider (qwen/opencode), API key, modelo
3. Guarda configuración en `~/.spec-gen/config.toml`

**Criterios de aceptación:**
- La API key nunca se muestra en pantalla (input oculto)
- La config se puede sobreescribir ejecutando `spec-gen config` de nuevo
- Soporta variable de entorno `SPEC_GEN_API_KEY` como alternativa

---

### UC-04 — Ver spec generada en terminal
**Actor:** Developer  
**Flujo:**
1. Developer ejecuta `spec-gen show --file requirements`
2. CLI imprime el contenido con syntax highlighting de Markdown

---

## 4. Requisitos no funcionales

| ID | Requisito |
|----|-----------|
| RNF-01 | Instalable con `pip install spec-gen` |
| RNF-02 | Compatible con Python 3.11+ |
| RNF-03 | Funciona offline si los archivos ya existen (UC-02, UC-04) |
| RNF-04 | Sin dependencias pesadas — solo Click, httpx, rich, tomllib |
| RNF-05 | Tiempo de respuesta < 30s en red normal |
| RNF-06 | Los archivos generados deben ser válidos para Kiro IDE y Claude Code |

---

## 5. Providers soportados (v1.0)

| Provider | Base URL | Modelos sugeridos |
|----------|----------|-------------------|
| Qwen (DashScope) | `https://dashscope.aliyuncs.com/compatible-mode/v1` | qwen-plus, qwen-turbo |
| Open Code | Configurable por el usuario | cualquiera compatible con OpenAI |

---

## 6. Fuera de alcance v1.0

- GUI o interfaz web
- Soporte para Claude API (v2.0)
- Integración con GitHub (crear repo + push automático)
- Validación semántica de la spec generada
- Internacionalización (solo español e inglés)

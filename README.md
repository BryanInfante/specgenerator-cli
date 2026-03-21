# spec-gen

CLI en Python que genera archivos de especificación SDD (REQUIREMENTS.md, DESIGN.md, TASKS.md)
desde una idea en lenguaje natural, usando LLMs.

## Instalación

```bash
pip install spec-gen
```

## Configuración

```bash
spec-gen config
export SPEC_GEN_API_KEY=tu-api-key
```

## Uso

```bash
spec-gen init "una API REST para gestionar tareas"
spec-gen config --show
```

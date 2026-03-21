import os
import tomllib
from pathlib import Path


class ConfigError(Exception):
    pass


class ApiKeyNotFoundError(ConfigError):
    pass


_CONFIG_DIR = Path.home() / ".spec-gen"
_CONFIG_FILE = _CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {
    "provider": {
        "name": "groq",
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
    },
    "output": {
        "language": "es",
        "overwrite": False,
    },
}


def load_config() -> dict:
    if not _CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()

    with open(_CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)

    for section, defaults in DEFAULT_CONFIG.items():
        if section not in config:
            config[section] = defaults
        else:
            for key, value in defaults.items():
                if key not in config[section]:
                    config[section][key] = value

    return config


def save_config(config: dict) -> None:
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    content = _toml.dumps(config)
    _CONFIG_FILE.write_text(content)


def get_api_key() -> str:
    api_key = os.environ.get("SPEC_GEN_API_KEY")
    if not api_key:
        raise ApiKeyNotFoundError(
            "La variable de entorno SPEC_GEN_API_KEY no está configurada.\n"
            "Configúrala con: export SPEC_GEN_API_KEY=tu-api-key"
        )
    return api_key


def mask_api_key(api_key: str) -> str:
    if len(api_key) <= 10:
        return "sk-****"
    return f"{api_key[:3]}****{api_key[-4:]}"


def _toml_from_string(s: str) -> dict:

    result = {}
    current_section = None

    for line in s.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1].strip()
            result[section_name] = {}
            current_section = section_name
        elif "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')

            if current_section:
                result[current_section][key] = value
            else:
                result[key] = value

    return result


def _get_toml_module():
    try:
        import tomllib

        return tomllib
    except ImportError:
        try:
            import tomli

            return tomli
        except ImportError:
            import toml

            return toml


class TomlWriter:
    @staticmethod
    def dumps(config: dict) -> str:
        lines = []
        for section, values in config.items():
            if isinstance(values, dict):
                lines.append(f"[{section}]")
                for key, value in values.items():
                    if isinstance(value, bool):
                        lines.append(f"{key} = {'true' if value else 'false'}")
                    elif isinstance(value, int):
                        lines.append(f"{key} = {value}")
                    else:
                        lines.append(f'{key} = "{value}"')
                lines.append("")
        return "\n".join(lines).rstrip() + "\n"


_toml = _get_toml_module()
if not hasattr(_toml, "dumps"):
    _toml.dumps = TomlWriter.dumps

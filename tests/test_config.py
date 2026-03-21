import os
from pathlib import Path
from unittest.mock import patch

import pytest

from spec_gen.config import (
    ApiKeyNotFoundError,
    DEFAULT_CONFIG,
    get_api_key,
    load_config,
    mask_api_key,
    save_config,
)


class TestMaskApiKey:
    def test_short_key(self):
        assert mask_api_key("sk-short") == "sk-****"

    def test_long_key(self):
        result = mask_api_key("sk-abc123def456ghi")
        assert result == "sk-****6ghi"

    def test_exactly_10_chars(self):
        result = mask_api_key("sk-1234567")
        assert result == "sk-****"


class TestLoadConfig:
    def test_load_config_with_valid_file(self, tmp_path, monkeypatch):
        config_dir = tmp_path / ".spec-gen"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"

        config_content = """[provider]
name = "opencode"
base_url = "https://api.example.com"
model = "custom-model"

[output]
language = "en"
overwrite = true
"""
        config_file.write_text(config_content)

        monkeypatch.setattr(
            "spec_gen.config._CONFIG_DIR", config_dir
        )
        monkeypatch.setattr(
            "spec_gen.config._CONFIG_FILE", config_file
        )

        config = load_config()

        assert config["provider"]["name"] == "opencode"
        assert config["provider"]["base_url"] == "https://api.example.com"
        assert config["provider"]["model"] == "custom-model"
        assert config["output"]["language"] == "en"
        assert config["output"]["overwrite"] is True

    def test_load_config_without_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("spec_gen.config._CONFIG_DIR", tmp_path / "nonexistent")
        monkeypatch.setattr(
            "spec_gen.config._CONFIG_FILE", tmp_path / "nonexistent" / "config.toml"
        )

        config = load_config()

        assert config == DEFAULT_CONFIG.copy()

    def test_load_config_partial_file(self, tmp_path, monkeypatch):
        config_dir = tmp_path / ".spec-gen"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"

        config_content = """[provider]
name = "qwen"
"""
        config_file.write_text(config_content)

        monkeypatch.setattr(
            "spec_gen.config._CONFIG_DIR", config_dir
        )
        monkeypatch.setattr(
            "spec_gen.config._CONFIG_FILE", config_file
        )

        config = load_config()

        assert config["provider"]["name"] == "qwen"
        assert "model" in config["provider"]


class TestGetApiKey:
    def test_get_api_key_with_env_var(self, monkeypatch):
        monkeypatch.setenv("SPEC_GEN_API_KEY", "sk-test-api-key-123")

        api_key = get_api_key()

        assert api_key == "sk-test-api-key-123"

    def test_get_api_key_without_env_var(self, monkeypatch):
        monkeypatch.delenv("SPEC_GEN_API_KEY", raising=False)

        with pytest.raises(ApiKeyNotFoundError) as exc_info:
            get_api_key()

        assert "SPEC_GEN_API_KEY no está configurada" in str(exc_info.value)


class TestSaveConfig:
    def test_save_config_creates_file(self, tmp_path, monkeypatch):
        config_dir = tmp_path / ".spec-gen"
        config_file = config_dir / "config.toml"

        monkeypatch.setattr("spec_gen.config._CONFIG_DIR", config_dir)
        monkeypatch.setattr("spec_gen.config._CONFIG_FILE", config_file)

        config_data = {
            "provider": {
                "name": "qwen",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                "model": "qwen-plus",
            },
            "output": {
                "language": "es",
                "overwrite": False,
            },
        }

        save_config(config_data)

        assert config_file.exists()
        content = config_file.read_text()
        assert "[provider]" in content
        assert "name = \"qwen\"" in content
        assert "[output]" in content
        assert "language = \"es\"" in content

from unittest.mock import MagicMock, patch

import httpx
import pytest

from spec_gen.providers import get_provider
from spec_gen.providers.base import (
    AuthenticationError,
    BaseProvider,
    RateLimitError,
    TimeoutError,
)
from spec_gen.providers.groq import GroqProvider
from spec_gen.providers.opencode import OpenCodeProvider
from spec_gen.providers.qwen import QwenProvider


class TestQwenProvider:
    @pytest.fixture
    def provider(self):
        return QwenProvider(
            api_key="test-key",
            model="qwen-plus",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    def test_complete_success(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Respuesta generada"}}]
        }

        with patch.object(provider._client, "post", return_value=mock_response):
            result = provider.complete("Hola, ¿cómo estás?")

        assert result == "Respuesta generada"

    def test_complete_auth_error(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch.object(provider._client, "post", return_value=mock_response):
            with pytest.raises(AuthenticationError) as exc_info:
                provider.complete("Hola")
            assert "API key inválida" in str(exc_info.value)

    def test_complete_rate_limit_error(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 429

        with patch.object(provider._client, "post", return_value=mock_response):
            with pytest.raises(RateLimitError) as exc_info:
                provider.complete("Hola")
            assert "Límite de solicitudes excedido" in str(exc_info.value)

    def test_complete_timeout_error(self, provider):
        with patch.object(
            provider._client, "post", side_effect=httpx.TimeoutException("timeout")
        ):
            with pytest.raises(TimeoutError) as exc_info:
                provider.complete("Hola")
            assert "Tiempo de espera agotado" in str(exc_info.value)

    def test_complete_server_error(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 500

        with patch.object(provider._client, "post", return_value=mock_response):
            with pytest.raises(TimeoutError) as exc_info:
                provider.complete("Hola")
            assert "Error del servidor" in str(exc_info.value)


class TestOpenCodeProvider:
    @pytest.fixture
    def provider(self):
        return OpenCodeProvider(
            api_key="test-key",
            model="custom-model",
            base_url="https://api.example.com",
        )

    def test_complete_success(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Respuesta generada"}}]
        }

        with patch.object(provider._client, "post", return_value=mock_response):
            result = provider.complete("Hola, ¿cómo estás?")

        assert result == "Respuesta generada"

    def test_complete_auth_error(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch.object(provider._client, "post", return_value=mock_response):
            with pytest.raises(AuthenticationError):
                provider.complete("Hola")


class TestGroqProvider:
    @pytest.fixture
    def provider(self):
        return GroqProvider(
            api_key="test-key",
            model="llama-3.3-70b-versatile",
            base_url="https://api.groq.com/openai/v1",
        )

    def test_complete_success(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Respuesta generada"}}]
        }

        with patch.object(provider._client, "post", return_value=mock_response):
            result = provider.complete("Hola, ¿cómo estás?")

        assert result == "Respuesta generada"

    def test_complete_auth_error(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch.object(provider._client, "post", return_value=mock_response):
            with pytest.raises(AuthenticationError) as exc_info:
                provider.complete("Hola")
            assert "API key inválida" in str(exc_info.value)

    def test_complete_rate_limit_error(self, provider):
        mock_response = MagicMock()
        mock_response.status_code = 429

        with patch.object(provider._client, "post", return_value=mock_response):
            with pytest.raises(RateLimitError) as exc_info:
                provider.complete("Hola")
            assert "Límite de solicitudes excedido" in str(exc_info.value)

    def test_complete_timeout_error(self, provider):
        with patch.object(
            provider._client, "post", side_effect=httpx.TimeoutException("timeout")
        ):
            with pytest.raises(TimeoutError) as exc_info:
                provider.complete("Hola")
            assert "Tiempo de espera agotado" in str(exc_info.value)


class TestGetProvider:
    def test_get_qwen_provider(self):
        config = {
            "api_key": "test-key",
            "provider": {
                "name": "qwen",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                "model": "qwen-plus",
            },
        }

        provider = get_provider(config)

        assert isinstance(provider, QwenProvider)
        assert provider.api_key == "test-key"
        assert provider.model == "qwen-plus"

    def test_get_opencode_provider(self):
        config = {
            "api_key": "test-key",
            "provider": {
                "name": "opencode",
                "base_url": "https://api.example.com",
                "model": "custom-model",
            },
        }

        provider = get_provider(config)

        assert isinstance(provider, OpenCodeProvider)
        assert provider.api_key == "test-key"
        assert provider.model == "custom-model"

    def test_get_groq_provider(self):
        config = {
            "api_key": "test-key",
            "provider": {
                "name": "groq",
                "base_url": "https://api.groq.com/openai/v1",
                "model": "llama-3.3-70b-versatile",
            },
        }

        provider = get_provider(config)

        assert isinstance(provider, GroqProvider)
        assert provider.api_key == "test-key"
        assert provider.model == "llama-3.3-70b-versatile"

    def test_get_unknown_provider(self):
        config = {
            "provider": {
                "name": "unknown",
                "base_url": "https://api.example.com",
                "model": "model",
            }
        }

        with pytest.raises(ValueError) as exc_info:
            get_provider(config)
        assert "Provider desconocido" in str(exc_info.value)


class TestBaseProvider:
    def test_base_provider_is_abstract(self):
        with pytest.raises(TypeError):
            BaseProvider("key", "model", "url")

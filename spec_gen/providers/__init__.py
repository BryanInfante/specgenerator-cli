from spec_gen.providers.base import (
    AuthenticationError,
    BaseProvider,
    ProviderError,
    RateLimitError,
    TimeoutError,
)
from spec_gen.providers.groq import GroqProvider
from spec_gen.providers.opencode import OpenCodeProvider
from spec_gen.providers.qwen import QwenProvider

AuthenticationError = AuthenticationError
ProviderError = ProviderError
RateLimitError = RateLimitError
TimeoutError = TimeoutError


def get_provider(config: dict) -> BaseProvider:
    provider_name = config["provider"]["name"]
    api_key = config.get("api_key", "")
    model = config["provider"]["model"]
    base_url = config["provider"]["base_url"]

    if provider_name == "qwen":
        return QwenProvider(api_key, model, base_url)
    elif provider_name == "groq":
        return GroqProvider(api_key, model, base_url)
    elif provider_name == "opencode":
        return OpenCodeProvider(api_key, model, base_url)
    else:
        raise ValueError(f"Provider desconocido: {provider_name}")

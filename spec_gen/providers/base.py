from abc import ABC, abstractmethod


class ProviderError(Exception):
    pass


class AuthenticationError(ProviderError):
    pass


class RateLimitError(ProviderError):
    pass


class TimeoutError(ProviderError):
    pass


class BaseProvider(ABC):
    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    @abstractmethod
    def complete(self, prompt: str) -> str:
        raise NotImplementedError

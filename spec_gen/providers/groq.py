import httpx

from spec_gen.providers.base import (
    AuthenticationError,
    BaseProvider,
    RateLimitError,
    TimeoutError,
)


class GroqProvider(BaseProvider):
    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        super().__init__(api_key, model, base_url)
        self._client = httpx.Client(timeout=60.0)

    def complete(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }

        try:
            response = self._client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
        except httpx.TimeoutException as e:
            raise TimeoutError(
                "Tiempo de espera agotado. "
                "Verifica tu conexión a internet e intenta de nuevo."
            ) from e

        if response.status_code == 401:
            raise AuthenticationError(
                "API key inválida. "
                "Verifica que SPEC_GEN_API_KEY esté configurada correctamente."
            )

        if response.status_code == 429:
            raise RateLimitError(
                "Límite de solicitudes excedido. "
                "Espera un momento antes de intentar de nuevo."
            )

        if response.status_code >= 500:
            raise TimeoutError(
                "Error del servidor del provider. Intenta de nuevo en unos minutos."
            )

        if response.status_code != 200:
            raise TimeoutError(
                f"Error inesperado (código {response.status_code}). Intenta de nuevo."
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def close(self) -> None:
        self._client.close()

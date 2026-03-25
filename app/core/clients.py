import httpx

from app.core.config import settings


class OpenRouterClient:
    def __init__(self):
        if not settings.openrouter_api_key:
            raise ValueError("Missing OPENROUTER_API_KEY in your .env file.")

        self.base_url = settings.openrouter_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }

        if settings.openrouter_site_url:
            self.headers["HTTP-Referer"] = settings.openrouter_site_url

        if settings.openrouter_app_title:
            self.headers["X-OpenRouter-Title"] = settings.openrouter_app_title

    def _post(self, path: str, payload: dict) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/{path.lstrip('/')}",
                headers=self.headers,
                json=payload,
                timeout=60.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"OpenRouter request failed with status {exc.response.status_code}: {exc.response.text}"
            ) from exc
        except httpx.HTTPError as exc:
            raise RuntimeError(f"OpenRouter request failed: {exc}") from exc

        return response.json()

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not settings.embedding_model:
            raise ValueError("Missing EMBEDDING_MODEL in your .env file.")

        response = self._post(
            "/embeddings",
            {
                "model": settings.embedding_model,
                "input": texts,
            },
        )

        return [item["embedding"] for item in response["data"]]

    def create_chat_completion(self, messages: list[dict], temperature: float = 0) -> str:
        response = self._post(
            "/chat/completions",
            {
                "model": settings.chat_model,
                "messages": messages,
                "temperature": temperature,
            },
        )

        return response["choices"][0]["message"]["content"]

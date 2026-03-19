from openai import OpenAI
from app.core.config import settings


class Embedder:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=[query]
        )
        return response.data[0].embedding

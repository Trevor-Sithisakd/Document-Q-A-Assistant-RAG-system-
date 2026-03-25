from app.core.clients import OpenRouterClient


class Embedder:
    def __init__(self):
        self.client = OpenRouterClient()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self.client.create_embeddings(texts)

    def embed_query(self, query: str) -> list[float]:
        return self.client.create_embeddings([query])[0]

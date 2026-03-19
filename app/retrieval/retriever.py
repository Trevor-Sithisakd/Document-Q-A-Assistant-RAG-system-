from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore


class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.store = ChromaStore()

    def retrieve(self, question: str, top_k: int = 4) -> list[dict]:
        query_embedding = self.embedder.embed_query(question)
        results = self.store.search(query_embedding, top_k=top_k)

        retrieved_chunks = []
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(documents, metadatas, distances):
            retrieved_chunks.append({
                "text": doc,
                "source": meta.get("source"),
                "page": meta.get("page"),
                "score": dist
            })

        return retrieved_chunks

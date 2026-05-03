import chromadb
from app.core.config import settings


class ChromaStore:
    def __init__(self, collection_name: str = "documents"):
        self.client = chromadb.PersistentClient(path=settings.vector_db_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        self.collection.add(
            ids=[chunk["chunk_id"] for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            embeddings=embeddings,
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
                for chunk in chunks
            ]
        )

    def source_exists(self, source: str) -> bool:
        results = self.collection.get(where={"source": source}, limit=1)
        return len(results["ids"]) > 0

    def delete_source(self, source: str) -> int:
        results = self.collection.get(where={"source": source})
        ids = results["ids"]
        if ids:
            self.collection.delete(ids=ids)
        return len(ids)

    def clear_all(self) -> int:
        results = self.collection.get()
        ids = results["ids"]
        if ids:
            self.collection.delete(ids=ids)
        return len(ids)

    def list_sources(self) -> list[str]:
        results = self.collection.get()
        return sorted({m["source"] for m in results["metadatas"] if m.get("source")})

    def search(self, query_embedding: list[float], top_k: int = 4) -> dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

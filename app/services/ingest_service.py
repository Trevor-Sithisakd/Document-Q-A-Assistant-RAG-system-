# coordinate the ingestion steps
import os
from app.core.config import settings
from app.ingestion.loader import load_pdf
from app.ingestion.cleaner import clean_text
from app.ingestion.chunker import chunk_pages
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore


class IngestService:
    def __init__(self):
        self.embedder = Embedder()
        self.store = ChromaStore()

    def ingest_document(self, file_path: str) -> dict:
        pages = load_pdf(file_path)

        cleaned_pages = [
            {"page": p["page"], "text": clean_text(p["text"])}
            for p in pages
        ]

        source = os.path.basename(file_path)

        chunks = chunk_pages(
            cleaned_pages,
            source=source,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap
        )

        embeddings = self.embedder.embed_texts([c["text"] for c in chunks])
        self.store.add_chunks(chunks, embeddings)

        return {
            "document_name": source,
            "pages": len(cleaned_pages),
            "chunks_created": len(chunks),
            "status": "success"
        }
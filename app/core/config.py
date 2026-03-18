from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Document Q&A Assistant"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    chat_model: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", 800))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", 100))
    vector_db_dir: str = os.getenv("VECTOR_DB_DIR", "data/vectordb")
    default_top_k: int = int(os.getenv("DEFAULT_TOP_K", 4))


settings = Settings()
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Document Q&A Assistant"
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "")
    chat_model: str = os.getenv("CHAT_MODEL", "openrouter/auto")
    openrouter_site_url: str = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501")
    openrouter_app_title: str = os.getenv("OPENROUTER_APP_TITLE", "Document Q&A Assistant")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", 800))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", 100))
    vector_db_dir: str = os.getenv("VECTOR_DB_DIR", "data/vectordb")
    default_top_k: int = int(os.getenv("DEFAULT_TOP_K", 4))


settings = Settings()

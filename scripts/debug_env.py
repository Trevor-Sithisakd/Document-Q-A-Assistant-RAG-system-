import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings

print(f"API Key loaded : {'YES - ' + settings.openrouter_api_key[:12] + '...' if settings.openrouter_api_key else 'NO - EMPTY'}")
print(f"Embedding model: {settings.embedding_model}")
print(f"Chat model     : {settings.chat_model}")
print(f"Base URL       : {settings.openrouter_base_url}")

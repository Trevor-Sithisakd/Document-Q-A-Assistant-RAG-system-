from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    question: str
    top_k: int = 4


class Citation(BaseModel):
    source: str
    page: int


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    latency_ms: float
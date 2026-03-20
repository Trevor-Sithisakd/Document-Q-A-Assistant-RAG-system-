#Coordinate retrieval + generation.
import time
from app.retrieval.retriever import Retriever
from app.generation.answer_generator import AnswerGenerator
from app.core.config import settings


class QueryService:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = AnswerGenerator()

    def answer_question(self, question: str, top_k: int | None = None) -> dict:
        start = time.time()

        top_k = top_k or settings.default_top_k
        contexts = self.retriever.retrieve(question, top_k=top_k)
        result = self.generator.generate_answer(question, contexts)

        latency_ms = round((time.time() - start) * 1000, 2)

        return {
            "answer": result["answer"],
            "citations": result["citations"],
            "used_chunks": result["used_chunks"],
            "latency_ms": latency_ms
        }
# call llm with retrived context
from app.core.clients import OpenRouterClient
from app.core.prompts import SYSTEM_PROMPT, build_user_prompt


class AnswerGenerator:
    def __init__(self):
        self.client = OpenRouterClient()

    def generate_answer(self, question: str, contexts: list[dict]) -> dict:
        user_prompt = build_user_prompt(question, contexts)

        answer = self.client.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0
        )

        citations = [
            {"source": c["source"], "page": c["page"]}
            for c in contexts
        ]

        return {
            "answer": answer,
            "citations": citations,
            "used_chunks": contexts
        }

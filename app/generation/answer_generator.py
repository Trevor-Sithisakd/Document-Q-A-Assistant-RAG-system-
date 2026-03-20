# call llm with retrived context
from openai import OpenAI
from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT, build_user_prompt


class AnswerGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.chat_model

    def generate_answer(self, question: str, contexts: list[dict]) -> dict:
        user_prompt = build_user_prompt(question, contexts)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        citations = [
            {"source": c["source"], "page": c["page"]}
            for c in contexts
        ]

        return {
            "answer": answer,
            "citations": citations,
            "used_chunks": contexts
        }
SYSTEM_PROMPT = """
You are an enterprise document question-answering assistant.

Answer only using the provided context.
If the answer is not supported by the context, say you do not know.
Always provide citations using source name and page number.
Do not fabricate facts.
"""

def build_user_prompt(question: str, contexts: list[dict]) -> str:
    context_text = "\n\n".join(
        [
            f"Source: {c['source']} | Page: {c['page']}\n{c['text']}"
            for c in contexts
        ]
    )

    return f"""
Question:
{question}

Context:
{context_text}

Instructions:
- Answer only from the context above.
- Include citations.
- If the context is insufficient, say so clearly.
"""
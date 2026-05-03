def citation_coverage(citations: list) -> float:
    return 1.0 if citations else 0.0


def latency_ok(latency_ms: float, threshold: float = 3000) -> bool:
    return latency_ms <= threshold


def no_answer_detected(answer: str) -> bool:
    """True if the model admitted it couldn't find an answer (expected behaviour for out-of-scope questions)."""
    phrases = ["i do not know", "i don't know", "not supported", "insufficient", "cannot find", "no information"]
    answer_lower = answer.lower()
    return any(p in answer_lower for p in phrases)


def faithfulness_score(answer: str, chunks: list[dict]) -> float:
    """
    Proxy for faithfulness: fraction of answer words that appear in the retrieved chunks.
    A low score suggests the model may have gone beyond the provided context.
    """
    if not chunks:
        return 0.0

    context_words = set()
    for chunk in chunks:
        context_words.update(chunk["text"].lower().split())

    answer_words = [w.strip(".,!?;:\"'()") for w in answer.lower().split()]
    if not answer_words:
        return 0.0

    matched = sum(1 for w in answer_words if w in context_words)
    return round(matched / len(answer_words), 2)


def retrieval_relevance(chunks: list[dict], threshold: float = 1.0) -> float:
    """
    Fraction of retrieved chunks whose distance score is below threshold.
    Chroma uses L2 distance — lower = more relevant.
    A score of 1.0 means all chunks were relevant; 0.0 means none were.
    """
    if not chunks:
        return 0.0
    relevant = sum(1 for c in chunks if c.get("score", 999) <= threshold)
    return round(relevant / len(chunks), 2)


def answer_length_ok(answer: str, min_words: int = 10, max_words: int = 500) -> bool:
    """Checks the answer is neither suspiciously short nor excessively long."""
    word_count = len(answer.split())
    return min_words <= word_count <= max_words


def keyword_coverage(answer: str, keywords: list[str]) -> float:
    """
    Fraction of expected keywords found in the answer.
    More granular than a single pass/fail keyword check.
    E.g. keywords=["Trevor", "Python", "FastAPI"] -> 0.67 if two of three found.
    """
    if not keywords:
        return 1.0
    answer_lower = answer.lower()
    matched = sum(1 for kw in keywords if kw.lower() in answer_lower)
    return round(matched / len(keywords), 2)


def source_diversity(citations: list[dict]) -> int:
    """Number of distinct source documents cited in the answer."""
    return len({c.get("source") for c in citations if c.get("source")})

def citation_coverage(citations: list) -> float:
    return 1.0 if citations else 0.0


def latency_ok(latency_ms: float, threshold: float = 3000) -> float:
    return 1.0 if latency_ms <= threshold else 0.0

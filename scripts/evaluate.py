"""
Run from the project root:  python scripts/evaluate.py

Evaluates the RAG pipeline against a set of test questions.
Each question has an expected keyword/phrase that should appear in the answer.

Metrics reported:
  - Keyword match   : answer contains the expected keyword (case-insensitive)
  - Citation coverage: response included at least one source citation
  - Latency         : response time in ms (pass = under 3000ms)
  - Overall accuracy: % of questions that passed all three checks
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.query_service import QueryService
from evaluation.metrics import citation_coverage, latency_ok

# --- Define your test questions here ---
# "expected" is a keyword/phrase you expect to appear in the answer.
TEST_CASES = [
    {
        "question": "What is this document about?",
        "expected": None,  # No keyword check, just tests it responds at all
    },
    # Add more once you know what's in your documents, e.g.:
    # {
    #     "question": "What is the candidate's name?",
    #     "expected": "Trevor",
    # },
    # {
    #     "question": "What does the parasympathetic nervous system do?",
    #     "expected": "rest",
    # },
]


def keyword_match(answer: str, expected: str | None) -> bool:
    if expected is None:
        return True
    return expected.lower() in answer.lower()


def run_evaluation():
    service = QueryService()

    results = []
    print(f"\nRunning {len(TEST_CASES)} test(s)...\n")
    print(f"{'#':<4} {'KEYWORD':<10} {'CITATION':<10} {'LATENCY':<10} QUESTION")
    print("-" * 70)

    for i, case in enumerate(TEST_CASES, 1):
        response = service.answer_question(case["question"])

        kw   = keyword_match(response["answer"], case["expected"])
        cite = citation_coverage(response["citations"]) == 1.0
        lat  = latency_ok(response["latency_ms"]) == 1.0
        passed = kw and cite and lat

        results.append(passed)

        kw_str   = "PASS" if kw   else "FAIL"
        cite_str = "PASS" if cite else "FAIL"
        lat_str  = f"{response['latency_ms']}ms" if lat else f"SLOW({response['latency_ms']}ms)"
        question_preview = case["question"][:40]

        print(f"{i:<4} {kw_str:<10} {cite_str:<10} {lat_str:<10} {question_preview}")

        if not kw and case["expected"]:
            print(f"     Expected keyword: '{case['expected']}'")
            print(f"     Answer preview  : {response['answer'][:120]}...")
        print()

    total   = len(results)
    passed  = sum(results)
    accuracy = (passed / total) * 100 if total else 0

    print("-" * 70)
    print(f"Overall accuracy: {passed}/{total} passed ({accuracy:.0f}%)\n")


if __name__ == "__main__":
    run_evaluation()

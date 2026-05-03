"""
Run from the project root:  python scripts/evaluate.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.query_service import QueryService
from evaluation.metrics import (
    citation_coverage,
    latency_ok,
    no_answer_detected,
    faithfulness_score,
    retrieval_relevance,
    answer_length_ok,
    keyword_coverage,
    source_diversity,
)

# --- Add your test questions here ---
# keywords: list of words you expect in the answer (empty list = skip keyword check)
# expect_no_answer: set True if the question is out of scope and the model should say "I don't know"
TEST_CASES = [
    {
        "question": "What is this document about?",
        "keywords": [],
        "expect_no_answer": False,
    },
    # Example with keyword check:
    # {
    #     "question": "What is the candidate's name?",
    #     "keywords": ["Trevor"],
    #     "expect_no_answer": False,
    # },
    # Example out-of-scope question (model should admit it doesn't know):
    # {
    #     "question": "What is the weather in Sydney today?",
    #     "keywords": [],
    #     "expect_no_answer": True,
    # },
]


def run_evaluation():
    service = QueryService()

    all_passed = []
    print(f"\nRunning {len(TEST_CASES)} test(s)...\n")

    for i, case in enumerate(TEST_CASES, 1):
        print(f"── Test {i}: {case['question']}")

        response = service.answer_question(case["question"])
        answer   = response["answer"]
        citations = response["citations"]
        chunks   = response["used_chunks"]
        latency  = response["latency_ms"]

        # Compute metrics
        kw_score    = keyword_coverage(answer, case["keywords"])
        faithful    = faithfulness_score(answer, chunks)
        relevance   = retrieval_relevance(chunks)
        has_cite    = citation_coverage(citations) == 1.0
        length_ok   = answer_length_ok(answer)
        fast        = latency_ok(latency)
        no_ans      = no_answer_detected(answer)
        diversity   = source_diversity(citations)

        # Pass/fail logic
        kw_pass      = kw_score == 1.0 or not case["keywords"]
        no_ans_pass  = (no_ans == case["expect_no_answer"])
        passed = kw_pass and has_cite and length_ok and fast and no_ans_pass

        all_passed.append(passed)

        # Print results
        print(f"   Keyword coverage  : {kw_score:.0%}" + (" (no keywords defined)" if not case["keywords"] else ""))
        print(f"   Faithfulness      : {faithful:.0%}  (how much of the answer came from retrieved chunks)")
        print(f"   Retrieval quality : {relevance:.0%}  (fraction of chunks that were close matches)")
        print(f"   Citation present  : {'YES' if has_cite else 'NO'}")
        print(f"   Source diversity  : {diversity} document(s) cited")
        print(f"   Answer length ok  : {'YES' if length_ok else 'NO'} ({len(answer.split())} words)")
        print(f"   Latency           : {latency}ms {'OK' if fast else 'SLOW'}")
        print(f"   No-answer detected: {'YES' if no_ans else 'NO'}" + (" (expected)" if case["expect_no_answer"] else ""))
        print(f"   Answer preview    : {answer[:150]}...")
        print(f"   Result            : {'PASS' if passed else 'FAIL'}")
        print()

    total    = len(all_passed)
    passed   = sum(all_passed)
    accuracy = (passed / total) * 100 if total else 0

    print("=" * 60)
    print(f"Overall: {passed}/{total} passed ({accuracy:.0f}%)")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation()

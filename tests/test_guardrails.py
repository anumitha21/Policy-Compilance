# tests/test_guardrails.py
import pytest
from guardrails.hallucination_guard import HallucinationGuard
from guardrails.policy_guard import PolicyGuard

class DummyLLM:
    def generate(self, prompt):
        # Return dummy JSON for testing
        return '{"is_grounded": true, "issues": []}'

@pytest.fixture
def retrieved_chunks():
    return [
        {"id": "1", "content": "Policy A: All audits must be annual.", "metadata": {"policy_title": "Policy A"}},
        {"id": "2", "content": "Policy B: Confidential data must be encrypted.", "metadata": {"policy_title": "Policy B"}}
    ]

def test_hallucination_guard(retrieved_chunks):
    guard = HallucinationGuard()
    guard.llm = DummyLLM()  # inject dummy LLM
    output_text = "All audits must be annual."
    result = guard.check_grounding(output_text, retrieved_chunks)
    assert result["is_grounded"] == True
    assert result["issues"] == []

def test_policy_guard(retrieved_chunks):
    valid_policies = [c["metadata"]["policy_title"] for c in retrieved_chunks]
    guard = PolicyGuard(valid_policies)
    citations = ["Policy A (ChunkID: 1)", "Fake Policy (ChunkID: 99)"]
    result = guard.filter_output("dummy", citations)
    assert result["is_valid"] == False
    assert "Fake Policy (ChunkID: 99)" in result["invalid_citations"]

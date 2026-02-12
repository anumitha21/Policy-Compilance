# config/prompts.py

COMPLIANCE_PROMPT = """
You are a compliance expert.
Analyze the following contract clause:

Clause:
{clause_text}

Against the following policy chunks:
{retrieved_chunks}

Provide:
- Compliance: Compliant / Non-Compliant / Partially Compliant
- Explanation (brief)
"""

RISK_PROMPT = """
You are a risk assessment expert.
Given the contract clause:

{clause_text}

And the following policy chunks:
{retrieved_chunks}

Provide a risk score from 0 (no risk) to 100 (high risk).
"""

SELF_REFINE_PROMPT = """
You are a compliance verification expert.
Review this output:

{output_text}

Based on the following policy chunks:
{retrieved_chunks}

Does the output accurately reflect the policies? If not, correct it.
"""

HALLUCINATION_CHECK_PROMPT = """
You are a compliance expert. 
Check if the following analysis output is fully supported by the given policy chunks.

Output:
{output_text}

Policy chunks:
{retrieved_chunks}

Instructions:
1. Identify any statements in the output that are NOT supported by the chunks.
2. Return a JSON with keys:
   - is_grounded: true/false
   - issues: list of unsupported statements
"""

# guardrails/hallucination_guard.py
from llm_client import LLMClient

class HallucinationGuard:
    def __init__(self, llm_model="llama-3.3-70b-versatile"):
        self.llm = LLMClient(model_name=llm_model)

    def check_grounding(self, output_text: str, retrieved_chunks: list[dict]) -> dict:
        """
        Checks if the LLM output is grounded in retrieved policy chunks.
        Returns:
            {
                "is_grounded": bool,
                "issues": list[str]  # unsupported statements
            }
        """
        context = "\n\n".join([f"[ChunkID {c['id']}]: {c['content']}" for c in retrieved_chunks])
        prompt = f"""
        You are a compliance expert. 
        Check if the following analysis output is fully supported by the given policy chunks.

        Output:
        {output_text}

        Policy chunks:
        {context}

        Instructions:
        1. Identify any statements in the output that are NOT supported by the chunks.
        2. Return a JSON with keys:
           - is_grounded: true/false
           - issues: list of unsupported statements
        """

        response = self.llm.generate(prompt)

        # For simplicity, assume the LLM returns valid JSON
        import json
        try:
            result = json.loads(response)
        except:
            result = {"is_grounded": False, "issues": ["Failed to parse LLM response."]}

        return result

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
        And the has to be Output ONLY valid JSON, and nothing else.
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

        # Robust JSON extraction
        import json, re
        def extract_json(text):
            # Try to find the first JSON object in the text
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception as e:
                    return None
            return None

        result = extract_json(response)
        if not result:
            result = {"is_grounded": False, "issues": ["Failed to parse LLM response.", f"Raw: {response}"]}

        return result

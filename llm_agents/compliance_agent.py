# llm_agents/compliance_agent.py
from llm_client import LLMClient  # wrapper for Groq / LLama Instant

class ComplianceAgent:
    def __init__(self, llm_model="llama-3.3-70b-versatile"):
        self.llm = LLMClient(model_name=llm_model)

    def analyze_clause(self, clause_text: str, retrieved_chunks: list[dict]):
        """
        Analyze a contract clause against policy chunks.
        Returns compliance classification and explanation as strict JSON.
        """
        # Prepare context
        context = "\n\n".join([f"[ChunkID {c['id']}]: {c['content']}" for c in retrieved_chunks])
        prompt = f"""
                You are a compliance expert. Your job is to strictly classify the compliance of a contract clause against policy requirements.

                Clause:
                {clause_text}

                Policy Chunks (context):
                {context}

                Instructions:
                - Output ONLY valid JSON, and nothing else.
                - The JSON must have the following keys:
                        compliance: "Compliant" | "Non-Compliant" | "Partially Compliant"
                        explanation: string (brief explanation)
                - "Compliant" means the clause fully satisfies all relevant policy requirements in the provided chunks.
                - "Non-Compliant" means the clause clearly violates or omits required policy elements.
                - "Partially Compliant" means the clause covers some, but not all, requirements, or is ambiguous.
                - If the policy chunks do not provide enough information, default to "Partially Compliant" and explain what is missing.
                - Example:
                    {{
                        "compliance": "Compliant",
                        "explanation": "The clause matches the policy requirements."
                    }}
                - Do not include any commentary or text outside the JSON object.
                """
        response = self.llm.generate(prompt)
        # Robust JSON parsing
        import json
        try:
            result = json.loads(response)
        except Exception as e:
            result = {
                "compliance": "Unknown",
                "explanation": f"Failed to parse LLM output as JSON: {str(e)}. Raw output: {response}"
            }
        return result

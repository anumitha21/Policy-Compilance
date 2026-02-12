# llm_agents/compliance_agent.py
from llm_client import LLMClient  # wrapper for Groq / LLama Instant

class ComplianceAgent:
    def __init__(self, llm_model="llama-3.3-70b-versatile"):
        self.llm = LLMClient(model_name=llm_model)

    def analyze_clause(self, clause_text: str, retrieved_chunks: list[dict]):
        """
        Analyze a contract clause against policy chunks.
        Returns compliance classification and explanation.
        """
        # Prepare context
        context = "\n\n".join([f"[ChunkID {c['id']}]: {c['content']}" for c in retrieved_chunks])
        prompt = f"""
        You are a compliance expert.
        Analyze the following contract clause:

        Clause:
        {clause_text}

        Against the following policy chunks:
        {context}

        Provide:
        - Compliance: Compliant / Non-Compliant / Partially Compliant
        - Explanation (brief)
        """
        response = self.llm.generate(prompt)
        return response

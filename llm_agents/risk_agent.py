# llm_agents/risk_agent.py
from llm_client import LLMClient

class RiskAgent:
    def __init__(self, llm_model="llama-3.3-70b-versatile"):
        self.llm = LLMClient(model_name=llm_model)

    def evaluate_risk(self, clause_text: str, retrieved_chunks: list[dict]):
        """
        Assigns a risk score (0-100) to the clause.
        """
        context = "\n\n".join([f"[ChunkID {c['id']}]: {c['content']}" for c in retrieved_chunks])
        prompt = f"""
        You are a risk assessment expert.
        Given the contract clause:

        {clause_text}

        And the following policy chunks:
        {context}

        Provide a risk score from 0 (no risk) to 100 (high risk).
        """
        response = self.llm.generate(prompt)
        return response

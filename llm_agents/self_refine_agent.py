# llm_agents/self_refine_agent.py
from llm_client import LLMClient

class SelfRefineAgent:
    def __init__(self, llm_model="llama-3.3-70b-versatile", max_iterations=2):
        self.llm = LLMClient(model_name=llm_model)
        self.max_iterations = max_iterations

    def refine(self, clause_text: str, initial_output: str, retrieved_chunks: list[dict]):
        """
        Checks if the LLM output is grounded in policy chunks.
        Refines the output if necessary.
        """
        context = "\n\n".join([f"[ChunkID {c['id']}]: {c['content']}" for c in retrieved_chunks])
        refined_output = initial_output

        for i in range(self.max_iterations):
            prompt = f"""
            You are a compliance verification expert.
            Review this output:

            {refined_output}

            Based on the following policy chunks:
            {context}

            Does the output accurately reflect the policies? If not, correct it.
            """
            refined_output = self.llm.generate(prompt)

        return refined_output

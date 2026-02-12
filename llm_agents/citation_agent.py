# llm_agents/citation_agent.py

class CitationAgent:
    def __init__(self):
        pass

    def generate_citations(self, retrieved_chunks: list[dict]):
        """
        Returns list of citations referencing chunk IDs and policy titles
        """
        citations = []
        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {})
            policy_title = metadata.get("policy_title", "Unknown Policy")
            citations.append(f"{policy_title} (ChunkID: {chunk['id']})")
        return citations

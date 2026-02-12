
# langgraph/graph.py
from langgraph.state import ClauseAnalysisState
from langgraph.nodes import (
    retrieval_node, reranker_node, compliance_node, risk_node,
    self_refine_node, citation_node, guardrails_node
)

class ContractCompliancePipeline:
    def __init__(self, retriever, reranker, compliance_agent, risk_agent, self_refine_agent, citation_agent):
        self.retriever = retriever
        self.reranker = reranker
        self.compliance_agent = compliance_agent
        self.risk_agent = risk_agent
        self.self_refine_agent = self_refine_agent
        self.citation_agent = citation_agent

    def run(self, clause_text: str):
        state = ClauseAnalysisState(clause_text=clause_text)

        # Run each node
        state = retrieval_node(state, self.retriever)
        state = reranker_node(state, self.reranker)
        state = compliance_node(state, self.compliance_agent)
        state = risk_node(state, self.risk_agent)
        state = self_refine_node(state, self.self_refine_agent)
        state = citation_node(state, self.citation_agent)
        state = guardrails_node(state)

        return state

# langgraph/nodes.py
from langgraph.state import ClauseAnalysisState
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker
from llm_agents.compliance_agent import ComplianceAgent
from llm_agents.risk_agent import RiskAgent
from llm_agents.self_refine_agent import SelfRefineAgent
from llm_agents.citation_agent import CitationAgent
from guardrails.hallucination_guard import HallucinationGuard
from guardrails.policy_guard import PolicyGuard

# ---------------- Retrieval Node ----------------
def retrieval_node(state: ClauseAnalysisState, retriever: HybridRetriever):
    state.retrieved_chunks = retriever.retrieve(state.clause_text, top_k=5)
    return state

# ---------------- Reranker Node ----------------
def reranker_node(state: ClauseAnalysisState, reranker: Reranker):
    state.reranked_chunks = reranker.rerank(state.clause_text, state.retrieved_chunks)
    return state

# ---------------- Compliance Node ----------------
def compliance_node(state: ClauseAnalysisState, agent: ComplianceAgent):
    state.initial_output = agent.analyze_clause(state.clause_text, state.reranked_chunks)
    return state

# ---------------- Risk Node ----------------
def risk_node(state: ClauseAnalysisState, agent: RiskAgent):
    state.risk_score = agent.evaluate_risk(state.clause_text, state.reranked_chunks)
    return state

# ---------------- Self-Refine Node ----------------
def self_refine_node(state: ClauseAnalysisState, agent: SelfRefineAgent):
    state.refined_output = agent.refine(state.clause_text, state.initial_output, state.reranked_chunks)
    return state

# ---------------- Citation Node ----------------
def citation_node(state: ClauseAnalysisState, agent: CitationAgent):
    state.citations = agent.generate_citations(state.reranked_chunks)
    return state

# ---------------- Guardrails Node ----------------
def guardrails_node(state: ClauseAnalysisState):
    hall_guard = HallucinationGuard()
    state.grounding_check = hall_guard.check_grounding(state.refined_output, state.reranked_chunks)

    valid_policies = [c["metadata"].get("policy_title", "Unknown") for c in state.reranked_chunks]
    policy_guard = PolicyGuard(valid_policies)
    state.policy_check = policy_guard.filter_output(state.refined_output, state.citations)

    return state

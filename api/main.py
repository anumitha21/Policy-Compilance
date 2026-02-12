# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from api.schemas import ClauseRequest, ClauseResponse
from langgraph.graph import ContractCompliancePipeline
from embeddings.vector_store import VectorStore
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker
from llm_agents.compliance_agent import ComplianceAgent
from llm_agents.risk_agent import RiskAgent
from llm_agents.self_refine_agent import SelfRefineAgent
from llm_agents.citation_agent import CitationAgent
import yaml

# Load settings
with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

# Initialize components
vector_store = VectorStore(persist_dir=settings["vector_store_dir"])
retriever = HybridRetriever(vector_store, index_dir=settings["bm25_index_dir"])
reranker = Reranker()
compliance_agent = ComplianceAgent(llm_model=settings["llm_model"])
risk_agent = RiskAgent(llm_model=settings["llm_model"])
self_refine_agent = SelfRefineAgent(llm_model=settings["llm_model"], max_iterations=settings["max_refine_iterations"])
citation_agent = CitationAgent()

pipeline = ContractCompliancePipeline(
    retriever, reranker, compliance_agent, risk_agent, self_refine_agent, citation_agent
)

# FastAPI app
app = FastAPI(title="Contract Compliance AI API")

class ClauseRequest(BaseModel):
    clause_text: str
@app.post("/analyze_clause/", response_model=ClauseResponse)
def analyze_clause(request: ClauseRequest):
    state = pipeline.run(request.clause_text)
    return ClauseResponse(
        refined_output=state.refined_output,
        risk_score=state.risk_score,
        citations=state.citations,
        grounding_check=state.grounding_check,
        policy_check=state.policy_check
    )

@app.get("/")
def root():
    return {"message": "Contract Compliance AI API is running."}

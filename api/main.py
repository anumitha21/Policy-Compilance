# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from api.schemas import ClauseRequest, ClauseResponse
from langgraph.graph import ContractCompliancePipeline
from embeddings.vector_store import PolicyVectorStore
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
vector_store = PolicyVectorStore(persist_directory=settings["vector_store_dir"])
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
from fastapi.responses import JSONResponse

@app.post("/analyze_clause/")
def analyze_clause(request: ClauseRequest):
    state = pipeline.run(request.clause_text)
    # Parse compliance output
    compliance = state.initial_output.get("compliance") if isinstance(state.initial_output, dict) else None
    explanation = state.initial_output.get("explanation") if isinstance(state.initial_output, dict) else ""
    # Only return if non-compliant
    if compliance != "Non-Compliant":
        return JSONResponse(content={"results": []})

    # Prepare evidence (no repeated chunk IDs)
    evidence = []
    seen_chunks = set()
    for chunk in state.reranked_chunks:
        chunk_id = chunk.get("id")
        if chunk_id in seen_chunks:
            continue
        seen_chunks.add(chunk_id)
        meta = chunk.get("metadata", {})
        evidence.append({
            "source": meta.get("policy_title", "GDPR-Guidance"),
            "article": meta.get("article", ""),
            "chunk_id": chunk_id,
            "excerpt": chunk.get("content", "")[:200]  # 1-2 lines only
        })

    result = {
        "clause_name": request.clause_text.split(":")[0].strip(),
        "compliance": compliance,
        "explanation": explanation,
        "risk_score": state.risk_score,
        "policy_evidence": evidence
    }
    return JSONResponse(content={"results": [result]})

@app.get("/")
def root():
    return {"message": "Contract Compliance AI API is running."}

# run_pipeline.py
from embeddings.embedder import create_embeddings
from embeddings.vector_store import ChromaVectorStore
from retrieval.chunk_loader import ChunkLoader
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker
from llm_agents.compliance_agent import ComplianceAgent
from llm_agents.risk_agent import RiskAgent
from llm_agents.self_refine_agent import SelfRefineAgent
from guardrails.hallucination_guard import HallucinationGuard

# -----------------------------
# 1. Load chunks
# -----------------------------
policy_chunks = ChunkLoader("data/policies/GDPR-Guidance.pdf")
contract_chunks = ChunkLoader("data/contracts/sample_contract_clauses.txt")

policy_texts, policy_ids = policy_chunks.get_texts_and_ids()
contract_texts, contract_ids = contract_chunks.get_texts_and_ids()

print(f"Loaded {len(policy_texts)} policy chunks")
print(f"Loaded {len(contract_texts)} contract chunks")

# -----------------------------
# 2. Create embeddings & vector store
# -----------------------------
embedding_model_name = "BGE-large-en"
embedder = create_embeddings(model_name=embedding_model_name)

vector_store = ChromaVectorStore()
vector_store.add_documents(policy_texts, policy_ids, embedder)

print("Policy embeddings stored in Chroma DB")

# -----------------------------
# 3. Initialize retriever + reranker
# -----------------------------
retriever = HybridRetriever(vector_store=vector_store, top_k=5)
reranker = Reranker(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")

# -----------------------------
# 4. Initialize agents
# -----------------------------
llm_model_name = "llama-3.3-70b-versatile"
compliance_agent = ComplianceAgent(llm_model=llm_model_name)
risk_agent = RiskAgent(llm_model=llm_model_name)
self_refine_agent = SelfRefineAgent(llm_model=llm_model_name, max_iterations=2)
hall_guard = HallucinationGuard(llm_model=llm_model_name)

# -----------------------------
# 5. Process each contract clause
# -----------------------------
results = []

for idx, clause in enumerate(contract_texts, start=1):
    print(f"\nProcessing clause {idx}: {clause[:60]}...")

    # Retrieve relevant policy chunks
    retrieved_chunks = retriever.retrieve(clause)
    reranked_chunks = reranker.rerank(clause, retrieved_chunks)

    # Run compliance agent
    compliance_result = compliance_agent.analyze_clause(clause, reranked_chunks)

    # Run risk agent
    risk_score = risk_agent.evaluate_risk(clause, reranked_chunks)

    # Run self-refine agent for verification
    refined_output = self_refine_agent.refine(clause, reranked_chunks, compliance_result)

    # Apply hallucination guard
    grounded_output = hall_guard.check(refined_output, reranked_chunks)

    # Collect citations (chunk IDs)
    citations = [chunk["id"] for chunk in reranked_chunks]

    results.append({
        "clause": clause,
        "compliance": grounded_output,
        "risk_score": risk_score,
        "citations": citations
    })

# -----------------------------
# 6. Print results
# -----------------------------
for idx, res in enumerate(results, start=1):
    print(f"\nClause {idx}: {res['clause'][:60]}...")
    print(f"Compliance Output: {res['compliance']}")
    print(f"Risk Score: {res['risk_score']}")
    print(f"Citations: {res['citations']}")


# run_pipeline.py
import os
from embeddings.vector_store import PolicyVectorStore
from retrieval.chunk_loader import ChunkLoader
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker
from llm_agents.compliance_agent import ComplianceAgent
from llm_agents.risk_agent import RiskAgent
from llm_agents.self_refine_agent import SelfRefineAgent
from guardrails.hallucination_guard import HallucinationGuard
from PyPDF2 import PdfReader

# -----------------------------
# 0. Utility: Convert PDF → TXT
# -----------------------------
def pdf_to_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# -----------------------------
# 1. Load policy and contract chunks
# -----------------------------
policy_pdf_path = "data/policies/GDPR-Guidance.pdf"
policy_txt_path = "data/policies/GDPR-Guidance.txt"

# Convert PDF to TXT if TXT does not exist
if not os.path.exists(policy_txt_path):
    policy_text = pdf_to_text(policy_pdf_path)
    with open(policy_txt_path, "w", encoding="utf-8") as f:
        f.write(policy_text)

# Load chunks
policy_chunks = ChunkLoader(policy_txt_path)
contract_chunks = ChunkLoader("data/contracts/sample_contract_clauses.txt")

policy_texts, policy_ids = policy_chunks.get_texts_and_ids()
contract_texts, contract_ids = contract_chunks.get_texts_and_ids()

# Convert IDs into metadata for Chroma
policy_metadata = [{"id": cid} for cid in policy_ids]

print(f"Loaded {len(policy_texts)} policy chunks")
print(f"Loaded {len(contract_texts)} contract chunks")

# -----------------------------
# 2. Create vector store and add policy chunks
# -----------------------------
vector_store = PolicyVectorStore(persist_directory="chroma_db")
vector_store.add_documents(policy_texts, policy_metadata)

print("Policy chunks added to Chroma vector store")

# -----------------------------
# 3. Initialize retriever + reranker
# -----------------------------
retriever = HybridRetriever(vector_store=vector_store)
reranker = Reranker(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")

# -----------------------------
# 4. Initialize LLM agents
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

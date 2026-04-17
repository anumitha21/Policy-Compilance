# 📑 Contract Compliance AI

An AI-powered system that analyzes contract clauses against company policies using a Retrieval-Augmented Generation (RAG) pipeline. The system provides compliance classification, risk scoring, and policy-backed explanations while ensuring outputs are grounded and reliable.

---

## 🚀 Overview

This project evaluates contract clauses by comparing them with relevant policy documents (e.g., GDPR).

The goal is to:
- Ensure every AI decision is backed by policy evidence  
- Prevent hallucinations using verification and guardrails  
- Provide explainable compliance and risk analysis  

---

## 🔄 Workflow

The system processes each contract clause through the following pipeline:

### 1. Input
- User provides a contract clause

### 2. Hybrid Retrieval
- Semantic search using embeddings (BGE + ChromaDB)
- Keyword search using BM25
- Retrieves top relevant policy chunks

### 3. Re-Ranking
- Uses cross-encoder model (`ms-marco-MiniLM-L-6-v2`)
- Selects Top 3 most relevant policy chunks

### 4. Compliance Analysis
- LLM compares:
  Contract Clause vs Policy Chunks
- Outputs:
  - Compliance (Compliant / Conflict / Missing)
  - Explanation
  - Risk Score
  - Policy Citations

### 5. Self-Refining Verification
- Second AI agent validates:
  - Correctness of citations
  - Logical consistency of output
- If incorrect, re-runs analysis (loop)

### 6. Guardrails
- Ensures structured output using Pydantic
- Prevents hallucinations
- Forces policy-grounded reasoning only

---

## 📤 Output

For each clause, the system returns:

- Clause  
- Compliance Result  
- Risk Score  
- Policy Citations (Chunk IDs)  
- Verified AI Output  

---

## ⭐ Key Features

- Hybrid Retrieval (BM25 + Vector Search)
- Cross-Encoder Re-Ranking for better precision
- Multi-Agent Architecture (Analyzer + Verifier)
- Self-Refining Loop for improved accuracy
- Hallucination Guardrails for safe AI output
- Risk Evaluation for legal insights
- Policy Citation-based explanations

---

## 🧰 Tech Stack

- LLM: Groq (llama-3.3-70b-versatile)
- Embeddings: BGE (bge-large-en)
- Vector Database: ChromaDB (LangChain wrapper)
- Retrieval: Hybrid (BM25 + Vector Search)
- Re-Ranker: cross-encoder/ms-marco-MiniLM-L-6-v2
- Orchestration: LangGraph
- Backend: FastAPI
- Frontend: Streamlit
- Validation: Pydantic
- Guardrails: Custom hallucination checks

---

## 📁 Project Structure
```bash
contract-compliance-ai/
│
├── data/                         # Input datasets
│   ├── policies/                # Policy documents (e.g., GDPR)
│   └── contracts/               # Sample contract clauses
│
├── embeddings/                  # Embedding & vector storage logic
│   ├── embedder.py              # BGE embedding model
│   └── vector_store.py          # ChromaDB integration
│
├── retrieval/                   # Retrieval pipeline
│   ├── hybrid_retriever.py      # BM25 + Vector search
│   ├── reranker.py              # Cross-encoder re-ranking
│   └── chunk_loader.py          # Chunk loading utility
│
├── llm_agents/                  # AI agents
│   ├── compliance_agent.py      # Compliance analysis
│   ├── risk_agent.py            # Risk scoring
│   └── self_refine_agent.py     # Verification & refinement loop
│
├── guardrails/                  # Safety & validation
│   └── hallucination_guard.py   # Grounding & hallucination check
│
├── langgraph/                   # Pipeline orchestration
│   ├── graph.py                 # Main workflow graph
│   ├── nodes.py                 # Individual pipeline nodes
│   └── state.py                 # Shared state management
│
├── api/                         # Backend API
│   ├── main.py                  # FastAPI entry point
│   └── schemas.py               # Request/response models
│
├── ui/                          # Frontend
│   └── streamlit_app.py         # Streamlit interface
│
├── config/                      # Configurations
│   ├── settings.yaml            # System settings
│   └── prompts.py               # LLM prompts
│
├── run_pipeline.py              # Standalone pipeline runner
├── requirements.txt             # Dependencies
└── README.md                    # Project documentation


---

## ⚙️ Setup

```bash
git clone <repo-url>
cd contract-compliance-ai

python -m venv myenv
myenv\Scripts\activate

pip install -r requirements.txt

## ⚙️ Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key

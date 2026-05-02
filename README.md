# Policy Compliance AI

An AI system that reads a company's contract clauses, checks them against internal policy documents, flags violations, scores the risk, and rewrites non-compliant clauses into corrected versions that align with the policy — all automatically.

Given a contract clause, the system retrieves the most relevant sections from the company's policy, determines whether the clause is compliant, assigns a risk score, cites the exact policy sections violated, and generates a suggested rewrite of the clause that is fully aligned with the policy — preserving the original intent while fixing the violation.

---

---

## Features

- **Compliance Detection** — Classifies each clause as `Compliant`, `Non-Compliant`, or `Partially Compliant`
- **Risk Scoring** — Assigns a risk score (0–100) to each non-compliant clause
- **Policy Evidence** — Shows the exact policy chunks that the clause was checked against
- **Hybrid Retrieval** — Combines keyword search (BM25) and semantic search (vector embeddings) for accurate policy chunk retrieval
- **Re-Ranking** — Re-scores retrieved chunks using a cross-encoder for higher relevance
- **Hallucination Control** — Verifies that the AI's output is grounded in actual policy text, not invented
- **Self-Refinement** — The AI reviews and corrects its own output up to 2 times before returning results
- **Suggested Clause Rewrite** — For every non-compliant clause, the system generates a corrected version that preserves the original intent but rewrites it to fully comply with the policy
- **Citation Tracking** — Every result is backed by a traceable policy chunk ID
- **REST API** — FastAPI backend for easy integration
- **Web UI** — Simple Streamlit interface for non-technical users

---

## How It Works

```
User inputs a contract clause
        │
        ▼
Hybrid Retrieval (BM25 + Vector Search)
→ Fetches top 5 relevant policy chunks
        │
        ▼
Re-Ranking (MiniLM Cross-Encoder)
→ Scores and sorts chunks by relevance
        │
        ▼
Compliance Agent (LLaMA 3.3 70B)
→ Compares clause vs policy chunks
→ Returns: Compliant / Non-Compliant / Partially Compliant + explanation
        │
        ▼
Risk Agent (LLaMA 3.3 70B)
→ Assigns risk score 0–100
        │
        ▼
Self-Refine Agent (2 iterations)
→ Verifies output is accurate against policy
→ Corrects if needed
        │
        ▼
Hallucination Guard
→ Flags any unsupported statements
→ Validates citations against known policies
        │
        ▼
Result returned to API → Displayed in UI
```

---

## Project Structure

```
Policy-Compliance/
│
├── data/
│   ├── policies/
│   │   └── GDPR-Guidance.pdf        # Company policy document
│   └── contracts/
│       └── sample_contract_clauses.txt  # Sample contract input
│
├── embeddings/
│   ├── embedder.py                  # BGE-large-en embedding model
│   └── vector_store.py              # ChromaDB vector store wrapper
│
├── retrieval/
│   ├── chunk_loader.py              # Loads and chunks PDF/TXT files
│   ├── hybrid_retriever.py          # BM25 (Whoosh) + vector search
│   └── reranker.py                  # MiniLM cross-encoder re-ranker
│
├── llm_agents/
│   ├── compliance_agent.py          # Classifies clause compliance
│   ├── risk_agent.py                # Scores risk (0–100)
│   ├── self_refine_agent.py         # Verifies and corrects LLM output
│   └── citation_agent.py            # Generates policy citations
│
├── guardrails/
│   ├── hallucination_guard.py       # Checks output is grounded in policy
│   └── policy_guard.py              # Validates citations are real
│
├── langgraph/
│   ├── state.py                     # Pipeline state (Pydantic model)
│   ├── nodes.py                     # Each pipeline step as a node
│   └── graph.py                     # Orchestrates the full pipeline
│
├── api/
│   ├── main.py                      # FastAPI app, /analyze_clause/ endpoint
│   └── schemas.py                   # Request/response models
│
├── ui/
│   └── streamlit_app.py             # Web interface
│
├── config/
│   ├── settings.yaml                # Model names, paths, parameters
│   └── prompts.py                   # LLM prompt templates
│
├── llm_client.py                    # Groq API wrapper
├── run_pipeline.py                  # Run pipeline directly (no API)
└── requirements.txt
```

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | LLaMA 3.3 70B via Groq |
| Embeddings | BAAI/bge-large-en-v1.5 |
| Vector DB | ChromaDB |
| Keyword Search | Whoosh (BM25) |
| Re-Ranker | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| Pipeline | LangGraph |
| Backend | FastAPI |
| Frontend | Streamlit |
| Validation | Pydantic |

---

## Setup

**1. Clone and create environment**
```bash
git clone <repo-url>
cd Policy-Compliance

python -m venv myenv
myenv\Scripts\activate        # Windows
source myenv/bin/activate     # Mac/Linux
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**

Create a `.env` file in the root:
```
GROQ_API_KEY=your_groq_api_key_here
```

---

## Running the Project

**Start the backend**
```bash
uvicorn api.main:app --reload
```

**Start the frontend** (in a new terminal)
```bash
cd ui
streamlit run streamlit_app.py
```

Then open `http://localhost:8501` in your browser, paste a contract clause, and click **Analyze Clause**.

---

## API

**POST** `/analyze_clause/`

Request:
```json
{
  "clause_text": "The company may share user data with third parties without explicit consent."
}
```

Response (if non-compliant):
```json
{
  "results": [
    {
      "clause_name": "Data Sharing Clause",
      "compliance": "Non-Compliant",
      "explanation": "Clause allows data sharing without consent, violating GDPR Article 6.",
      "risk_score": "85",
      "policy_evidence": [
        {
          "source": "GDPR-Guidance",
          "chunk_id": "12",
          "excerpt": "Personal data shall be processed lawfully... consent of the data subject."
        }
      ]
    }
  ]
}
```

Response (if compliant):
```json
{ "results": [] }
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key for LLaMA access |

---

## Notes

- Only **GDPR-Guidance.pdf** is used as the policy document by default. To use a different policy, replace the file in `data/policies/` and update the path in `run_pipeline.py`.
- The system currently flags and returns only **Non-Compliant** clauses via the API. Compliant clauses return an empty result.
- All model names, paths, and parameters are configurable via `config/settings.yaml` — no code changes needed.

---

## License

This project is for internal/educational use. Not intended as legal advice.

---

> Built with LLaMA 3.3 70B · ChromaDB · LangGraph · FastAPI · Streamlit

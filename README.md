# 📑 Policy Compliance AI

> An intelligent AI-powered system that analyzes contract clauses against company policies using Retrieval-Augmented Generation (RAG), providing compliance decisions, risk scoring, and policy-backed explanations with strong hallucination control.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange)

---

## 📌 Overview

**Contract Compliance AI** is a system that evaluates contract clauses by comparing them with company policy documents (e.g., GDPR).

It ensures:
- AI outputs are **grounded in policy evidence**
- No hallucinated or unsupported claims
- Reliable results using **multi-agent verification**

---

## ✨ Features

### 📜 Contract Analysis
- Input any contract clause
- AI evaluates compliance against company policies
- Supports real-world legal use cases

### 🔍 Hybrid Retrieval
- Combines:
  - Semantic search (BGE embeddings)
  - Keyword search (BM25)
- Retrieves relevant policy chunks

### 🎯 Re-Ranking
- Uses **cross-encoder/ms-marco-MiniLM-L-6-v2**
- Selects top relevant policy sections

### 🤖 AI Compliance Engine
- Powered by **Groq LLaMA 3.3 70B**
- Outputs:
  - Compliance classification
  - Explanation
  - Risk score
  - Policy citations

### 🔁 Self-Refining Verification
- Second AI agent validates output
- Ensures logical consistency
- Re-runs analysis if needed

### 🛡️ Guardrails
- Prevents hallucinations
- Ensures outputs are policy-grounded
- Structured output validation using Pydantic

---

## 🔄 System Workflow

1. User inputs a contract clause  
2. Hybrid retriever finds relevant policy chunks  
3. Cross-encoder re-ranks results  
4. LLM analyzes compliance  
5. Verification agent validates output  
6. Guardrails ensure safe and structured output  

---

## 🛠 Tech Stack

| Layer | Technology |
|------|-----------|
| **LLM** | Groq — LLaMA 3.3 70B Versatile |
| **Embeddings** | BGE (bge-large-en) |
| **Vector DB** | ChromaDB |
| **Retrieval** | Hybrid (BM25 + Vector Search) |
| **Re-Ranker** | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| **Pipeline** | LangGraph |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **Validation** | Pydantic |
| **Guardrails** | Custom hallucination checks |

---

## 📁 Project Structure

```bash
contract-compliance-ai/
│
├── data/                         # Policy & contract data
│   ├── policies/
│   └── contracts/
│
├── embeddings/                  # Embedding + vector DB
│   ├── embedder.py
│   └── vector_store.py
│
├── retrieval/                   # Retrieval logic
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   └── chunk_loader.py
│
├── llm_agents/                  # AI agents
│   ├── compliance_agent.py
│   ├── risk_agent.py
│   └── self_refine_agent.py
│
├── guardrails/                  # Safety checks
│   └── hallucination_guard.py
│
├── langgraph/                   # Pipeline orchestration
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── api/                         # FastAPI backend
│   ├── main.py
│   └── schemas.py
│
├── ui/                          # Streamlit frontend
│   └── streamlit_app.py
│
├── config/                      # Config & prompts
│   ├── settings.yaml
│   └── prompts.py
│
├── run_pipeline.py
├── requirements.txt
└── README.md
'''
⚙️ Environment Setup

Create a .env file in the root directory:

GROQ_API_KEY=your_api_key
🚀 Getting Started
Installation
git clone <repo-url>
cd contract-compliance-ai

python -m venv myenv
myenv\Scripts\activate

pip install -r requirements.txt
▶️ Run the Project
🚀 Start Backend
uvicorn api.main:app --reload
💻 Run Frontend
cd ui
streamlit run streamlit_app.py
🧠 AI Capabilities
Feature	Model
Compliance Analysis	LLaMA 3.3 70B
Risk Evaluation	LLaMA 3.3 70B
Retrieval Embeddings	BGE-large-en
Re-Ranking	MiniLM Cross Encoder
💡 Uniqueness
Combines RAG + Multi-Agent Verification
Uses Self-Refining Loop
Ensures 100% policy-grounded outputs
Includes hallucination guardrails
Designed for enterprise legal AI systems

## 🤝 Contributing

Contributions are welcome! 🚀

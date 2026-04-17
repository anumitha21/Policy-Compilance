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

### 🔍 Hybrid Retrieval
- Semantic search (BGE embeddings)
- Keyword search (BM25)

### 🎯 Re-Ranking
- cross-encoder/ms-marco-MiniLM-L-6-v2

### 🤖 AI Compliance Engine
- LLaMA 3.3 70B (Groq)
- Outputs compliance, explanation, risk, citations

### 🔁 Self-Refining Verification
- Validates and improves outputs

### 🛡️ Guardrails
- Prevents hallucination
- Ensures structured output

---

## 🔄 System Workflow

1. Input contract clause  
2. Retrieve policy chunks  
3. Re-rank results  
4. LLM analyzes compliance  
5. Verification loop  
6. Guardrail validation  

---

## 🛠 Tech Stack

- LLM: Groq (LLaMA 3.3 70B)
- Embeddings: BGE-large-en
- Vector DB: ChromaDB
- Retrieval: Hybrid (BM25 + Vector)
- Re-Ranker: MiniLM Cross Encoder
- Pipeline: LangGraph
- Backend: FastAPI
- Frontend: Streamlit
- Validation: Pydantic

---

## 📁 Project Structure

```bash
contract-compliance-ai/
│
├── data/
│   ├── policies/
│   └── contracts/
│
├── embeddings/
│   ├── embedder.py
│   └── vector_store.py
│
├── retrieval/
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   └── chunk_loader.py
│
├── llm_agents/
│   ├── compliance_agent.py
│   ├── risk_agent.py
│   └── self_refine_agent.py
│
├── guardrails/
│   └── hallucination_guard.py
│
├── langgraph/
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── api/
│   ├── main.py
│   └── schemas.py
│
├── ui/
│   └── streamlit_app.py
│
├── config/
│   ├── settings.yaml
│   └── prompts.py
│
├── run_pipeline.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Environment Setup

```env
GROQ_API_KEY=your_api_key
```

---

## 🚀 Getting Started

```bash
git clone <repo-url>
cd contract-compliance-ai

python -m venv myenv
myenv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run the Project

### Backend

```bash
uvicorn api.main:app --reload
```

### Frontend

```bash
cd ui
streamlit run streamlit_app.py
```

---

## 🧠 AI Capabilities

- Compliance Analysis — LLaMA 3.3  
- Risk Evaluation — LLaMA 3.3  
- Retrieval — BGE embeddings  
- Re-ranking — MiniLM cross encoder  

---


## 🤝 Contributing

Contributions are welcome!

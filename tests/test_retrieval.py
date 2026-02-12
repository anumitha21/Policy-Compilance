# tests/test_retrieval.py
import pytest
from retrieval.chunk_loader import ChunkLoader
from embeddings.vector_store import VectorStore
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker

@pytest.fixture
def sample_chunks():
    return [
        {"id": "1", "text": "Policy A: All audits must be annual.", "metadata": {"policy_title": "Policy A"}},
        {"id": "2", "text": "Policy B: Confidential data must be encrypted.", "metadata": {"policy_title": "Policy B"}}
    ]

def test_chunk_loader(tmp_path, sample_chunks):
    # Save sample chunks to json
    import json
    file_path = tmp_path / "chunks.json"
    with open(file_path, "w") as f:
        json.dump(sample_chunks, f)

    loader = ChunkLoader(str(file_path))
    chunks = loader.get_chunks()
    assert len(chunks) == 2
    assert chunks[0]["id"] == "1"

def test_hybrid_retriever(tmp_path, sample_chunks):
    texts = [c["text"] for c in sample_chunks]
    ids = [c["id"] for c in sample_chunks]

    vector_store = VectorStore(persist_dir=str(tmp_path / "chroma_db"))
    retriever = HybridRetriever(vector_store, index_dir=str(tmp_path / "whoosh_index"))
    retriever.add_documents(texts, ids)

    results = retriever.retrieve("audit")
    assert len(results) > 0
    assert any("audit" in r["content"].lower() for r in results)

def test_reranker(sample_chunks):
    reranker = Reranker()
    query = "audit compliance"
    reranked = reranker.rerank(query, sample_chunks)
    assert len(reranked) == len(sample_chunks)
    # Scores should be sorted descending
    scores = [doc["score"] for doc in reranked]
    assert scores == sorted(scores, reverse=True)

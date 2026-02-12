# retrieval/reranker.py
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, docs: list[dict]):
        """Rerank docs based on relevance to query"""
        pairs = [[query, doc["content"]] for doc in docs]
        scores = self.model.predict(pairs)
        for doc, score in zip(docs, scores):
            doc["score"] = score
        docs.sort(key=lambda x: x["score"], reverse=True)
        return docs

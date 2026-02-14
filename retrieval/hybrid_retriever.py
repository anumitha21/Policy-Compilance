# retrieval/hybrid_retriever.py
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from embeddings.vector_store import PolicyVectorStore

class HybridRetriever:
    def __init__(self, vector_store: PolicyVectorStore, index_dir="whoosh_index"):
        self.vector_store = vector_store
        self.index_dir = index_dir

        # Whoosh BM25 setup
        try:
            self.ix = open_dir(index_dir)
        except:
            from os import mkdir
            mkdir(index_dir)
            schema = Schema(id=ID(stored=True), content=TEXT(stored=True))
            self.ix = create_in(index_dir, schema)

    def add_documents(self, docs: list[str], doc_ids: list[str]):
        """Add documents to BM25 index"""
        writer = self.ix.writer()
        for doc_id, doc in zip(doc_ids, docs):
            writer.add_document(id=doc_id, content=doc)
        writer.commit()

        # Add to vector DB as well
        metadata = [{"id": doc_id} for doc_id in doc_ids]
        self.vector_store.add_documents(docs, metadata)

    def retrieve(self, query: str, top_k=5):
        """Hybrid retrieval: BM25 + Vector similarity"""
        # BM25 search
        qp = QueryParser("content", schema=self.ix.schema)
        q = qp.parse(query)
        bm25_results = []
        with self.ix.searcher() as searcher:
            hits = searcher.search(q, limit=top_k)
            for hit in hits:
                bm25_results.append({"id": hit["id"], "content": hit["content"]})

        # Vector search
        vector_results = self.vector_store.similarity_search(query, k=top_k)

        # Convert LangChain Document objects to dicts with 'id' and 'content'
        def doc_to_dict(doc):
            # Try to extract id from metadata if present
            doc_id = doc.metadata.get("id") if hasattr(doc, "metadata") and isinstance(doc.metadata, dict) else None
            return {"id": doc_id, "content": getattr(doc, "page_content", str(doc))}

        if isinstance(vector_results, list):
            if all(hasattr(item, "page_content") for item in vector_results):
                vector_results_dicts = [doc_to_dict(doc) for doc in vector_results]
                combined_results = bm25_results + vector_results_dicts
            elif all(isinstance(item, dict) for item in vector_results):
                combined_results = bm25_results + vector_results
            else:
                combined_results = bm25_results + [{"id": None, "content": str(doc)} for doc in vector_results]
        else:
            combined_results = bm25_results

        return combined_results[:top_k]

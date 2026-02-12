# embeddings/vector_store.py
from chromadb import Client
from chromadb.config import Settings
from embeddings.embedder import Embedder

class VectorStore:
    def __init__(self, persist_dir="chroma_db"):
        self.client = Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir
        ))
        self.collection = self.client.get_or_create_collection(name="policies")
        self.embedder = Embedder()

    def add_documents(self, docs: list[str], metadata: list[dict]):
        """Add docs to Chroma vector DB"""
        embeddings = self.embedder.embed_documents(docs)
        self.collection.add(
            documents=docs,
            embeddings=embeddings,
            metadatas=metadata
        )

    def similarity_search(self, query: str, k=5):
        """Retrieve top-k most similar documents"""
        query_embedding = self.embedder.embed_text(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results

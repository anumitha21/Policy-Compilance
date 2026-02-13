# embeddings/vector_store.py

from langchain_chroma import Chroma
from embeddings.embedder import create_embeddings

class PolicyVectorStore:
    """
    Wrapper for Chroma vector store for policy texts
    """
    def __init__(self, persist_directory="chroma_db", model_name="BAAI/bge-large-en-v1.5"):
        self.embedding_model = create_embeddings(model_name)
        self.collection = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model,
            collection_name="policies"
        )

    def add_documents(self, docs, metadata):
        """
        Add policy texts and their metadata
        """
        self.collection.add_texts(
            texts=docs,
            metadatas=metadata
        )

    def similarity_search(self, query, k=5):
        """
        Retrieve top-k similar policies for a query
        """
        return self.collection.similarity_search(query, k=k)

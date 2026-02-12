from langchain.embeddings import HuggingFaceEmbeddings

class Embedder:
    def __init__(self):
        # Use BigScience BGE model
        self.embedder = HuggingFaceEmbeddings(model_name="BGE-large-en")

    def embed_text(self, text: str):
        """Generate embedding for a single text string"""
        return self.embedder.embed_query(text)

    def embed_documents(self, docs: list[str]):
        """Generate embeddings for a list of documents"""
        return self.embedder.embed_documents(docs)

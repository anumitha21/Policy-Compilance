# embeddings/embedder.py
from transformers import AutoTokenizer, AutoModel
import torch
from langchain.embeddings.base import Embeddings

class BGEEmbedder(Embeddings):
    """
    HuggingFace BGE Embeddings wrapper compatible with LangChain.
    Implements embed_documents() and embed_query().
    """
    def __init__(self, model_name="BAAI/bge-large-en-v1.5", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def _embed_text(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True, return_dict=True)
            # Mean pooling over last hidden state
            embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.cpu().numpy()[0]

    def embed_documents(self, texts):
        return [self._embed_text(t) for t in texts]

    def embed_query(self, text):
        return self._embed_text(text)

# Helper function
def create_embeddings(model_name="BAAI/bge-large-en-v1.5"):
    return BGEEmbedder(model_name)

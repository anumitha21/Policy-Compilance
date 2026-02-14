# retrieval/chunk_loader.py
import json
import os
from typing import List, Dict
import PyPDF2  # for PDF reading

class ChunkLoader:
    def __init__(self, file_path: str, chunk_size: int = 300, chunk_overlap: int = 50, clause_mode: bool = False):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.clause_mode = clause_mode
        self.chunks = self._load_chunks()

    def _load_chunks(self) -> List[Dict]:
        """Load chunks from JSON, TXT, or PDF file"""
        if self.file_path.endswith(".json"):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        elif self.file_path.endswith(".txt"):
            return self._load_txt()

        elif self.file_path.endswith(".pdf"):
            return self._load_pdf()

        else:
            raise ValueError("Unsupported file type. Must be .json, .txt, or .pdf")

    def _split_text(self, text: str) -> List[str]:
        # Split text into overlapping chunks
        chunks = []
        start = 0
        length = len(text)
        while start < length:
            end = min(start + self.chunk_size, length)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def _load_txt(self) -> List[Dict]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            full_text = f.read()
        if self.clause_mode:
            # Split by numbered clauses (e.g., '1. ...', '2. ...')
            import re
            clause_pattern = r"(?:^|\n)(\d+\. .+?)(?=(?:\n\d+\. )|\Z)"
            matches = re.findall(clause_pattern, full_text, re.DOTALL)
            chunks = []
            for idx, clause in enumerate(matches, 1):
                clause = clause.strip()
                if clause:
                    chunks.append({
                        "id": str(idx),
                        "text": clause,
                        "metadata": {"source": os.path.basename(self.file_path)}
                    })
            return chunks
        else:
            text_chunks = self._split_text(full_text)
            chunks = []
            for idx, chunk in enumerate(text_chunks, 1):
                chunks.append({
                    "id": str(idx),
                    "text": chunk,
                    "metadata": {"source": os.path.basename(self.file_path)}
                })
            return chunks

    def _load_pdf(self) -> List[Dict]:
        chunks = []
        with open(self.file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            chunk_id = 0
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text:
                    text_chunks = self._split_text(text)
                    for chunk in text_chunks:
                        chunk_id += 1
                        chunks.append({
                            "id": f"{page_num}-{chunk_id}",
                            "text": chunk,
                            "metadata": {
                                "source": os.path.basename(self.file_path),
                                "page": page_num
                            }
                        })
        return chunks

    def get_chunks(self) -> List[Dict]:
        return self.chunks

    def get_texts_and_ids(self):
        texts = [chunk["text"] for chunk in self.chunks]
        ids = [chunk["id"] for chunk in self.chunks]
        return texts, ids

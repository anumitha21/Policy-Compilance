# retrieval/chunk_loader.py
import json
import os
from typing import List, Dict
import PyPDF2  # for PDF reading

class ChunkLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
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

    def _load_txt(self) -> List[Dict]:
        chunks = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            chunk_id = 0
            for line in f:
                line = line.strip()
                if line:
                    chunk_id += 1
                    chunks.append({
                        "id": str(chunk_id),
                        "text": line,
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
                    for line in text.split("\n"):
                        line = line.strip()
                        if line:
                            chunk_id += 1
                            chunks.append({
                                "id": f"{page_num}-{chunk_id}",
                                "text": line,
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

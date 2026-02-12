# langgraph/state.py
from pydantic import BaseModel
from typing import List, Dict

class ClauseAnalysisState(BaseModel):
    clause_text: str
    retrieved_chunks: List[Dict] = []
    reranked_chunks: List[Dict] = []
    initial_output: str = ""
    risk_score: str = ""
    refined_output: str = ""
    citations: List[str] = []
    grounding_check: Dict = {}
    policy_check: Dict = {}

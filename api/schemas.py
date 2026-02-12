# api/schemas.py
from pydantic import BaseModel
from typing import List, Dict

class ClauseRequest(BaseModel):
    clause_text: str

class ClauseResponse(BaseModel):
    refined_output: str
    risk_score: str
    citations: List[str]
    grounding_check: Dict
    policy_check: Dict

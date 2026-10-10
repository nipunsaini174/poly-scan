from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ActionNode(BaseModel):
    id: int
    action_type: str
    details: Dict[str, Any] = {}
    original_code: str = ""
    line_number: int = -1

class BehaviorGraphModel(BaseModel):
    nodes: List[ActionNode]
    edges: List[Dict[str, int]]  # {"source": id, "target": id}
    
class SimilarityResult(BaseModel):
    similarity_percentage: float
    matched_actions: List[str]
    unique_to_a: List[str]
    unique_to_b: List[str]
    graph_similarity: float
    explanation: str

class AnalyzeRequest(BaseModel):
    code_a: str = Field(..., max_length=100000, description="Source code A")
    language_a: str = Field(..., description="Language of code A (python, javascript)")
    code_b: str = Field(..., max_length=100000, description="Source code B")
    language_b: str = Field(..., description="Language of code B (python, javascript)")

class AnalyzeResponse(BaseModel):
    language_a: str
    language_b: str
    tags_a: List[str]
    tags_b: List[str]
    graph_a: BehaviorGraphModel
    graph_b: BehaviorGraphModel
    similarity: SimilarityResult
    error: Optional[str] = None

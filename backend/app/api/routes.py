from fastapi import APIRouter, HTTPException, status
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, BehaviorGraphModel, SimilarityResult
from app.parsers.python_parser import PythonParser
from app.parsers.javascript_parser import JavaScriptParser
from app.analyzer.behavior_graph import build_behavior_graph
from app.analyzer.similarity import calculate_similarity

router = APIRouter()

def get_parser(language: str):
    lang = language.lower()
    if lang == "python":
        return PythonParser()
    elif lang == "javascript":
        return JavaScriptParser()
    return None

def analyze_code_pair(req: AnalyzeRequest) -> AnalyzeResponse:
    if not req.code_a.strip() or not req.code_b.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Source code cannot be empty")
        
    parser_a = get_parser(req.language_a)
    parser_b = get_parser(req.language_b)
    
    if not parser_a:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported language: {req.language_a}")
    if not parser_b:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported language: {req.language_b}")
        
    try:
        nodes_a = parser_a.parse(req.code_a)
        nodes_b = parser_b.parse(req.code_b)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    graph_a = build_behavior_graph(nodes_a)
    graph_b = build_behavior_graph(nodes_b)
    
    tags_a = [n.action_type for n in nodes_a]
    tags_b = [n.action_type for n in nodes_b]
    
    similarity = calculate_similarity(graph_a, graph_b)
    
    return AnalyzeResponse(
        language_a=req.language_a,
        language_b=req.language_b,
        tags_a=tags_a,
        tags_b=tags_b,
        graph_a=graph_a,
        graph_b=graph_b,
        similarity=similarity
    )

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(req: AnalyzeRequest):
    return analyze_code_pair(req)

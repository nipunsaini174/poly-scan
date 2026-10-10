import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.schemas import AnalyzeRequest
from app.api.routes import get_parser
from app.analyzer.behavior_graph import build_behavior_graph
from app.analyzer.similarity import calculate_similarity

router = APIRouter()

@router.websocket("/ws/analyze")
async def analyze_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                req_dict = json.loads(data)
                req = AnalyzeRequest(**req_dict)
                
                await websocket.send_text(json.dumps({"stage": "Parsing Code A..."}))
                await asyncio.sleep(0.5) # Artificial delay for UI UX 
                parser_a = get_parser(req.language_a)
                if not parser_a:
                    await websocket.send_text(json.dumps({"error": f"Unsupported language A: {req.language_a}"}))
                    continue
                nodes_a = parser_a.parse(req.code_a)
                
                await websocket.send_text(json.dumps({"stage": "Parsing Code B..."}))
                await asyncio.sleep(0.5)
                parser_b = get_parser(req.language_b)
                if not parser_b:
                    await websocket.send_text(json.dumps({"error": f"Unsupported language B: {req.language_b}"}))
                    continue
                nodes_b = parser_b.parse(req.code_b)
                

                
                await websocket.send_text(json.dumps({"stage": "Extracting behavioral actions..."}))
                await asyncio.sleep(0.5)
                
                await websocket.send_text(json.dumps({"stage": "Building behavior graphs..."}))
                await asyncio.sleep(0.5)
                graph_a = build_behavior_graph(nodes_a)
                graph_b = build_behavior_graph(nodes_b)
                
                await websocket.send_text(json.dumps({"stage": "Comparing behavioral fingerprints..."}))
                await asyncio.sleep(0.5)
                similarity = calculate_similarity(graph_a, graph_b)
                
                tags_a = [n.action_type for n in nodes_a]
                tags_b = [n.action_type for n in nodes_b]
                
                await websocket.send_text(json.dumps({"stage": "Analysis complete."}))
                
                # Send the final result
                result = {
                    "language_a": req.language_a,
                    "language_b": req.language_b,
                    "tags_a": tags_a,
                    "tags_b": tags_b,
                    "graph_a": graph_a.model_dump(),
                    "graph_b": graph_b.model_dump(),
                    "similarity": similarity.model_dump()
                }
                
                await websocket.send_text(json.dumps({"result": result}))
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON format"}))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
                
    except WebSocketDisconnect:
        pass

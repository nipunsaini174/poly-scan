from typing import List
from app.models.schemas import ActionNode, BehaviorGraphModel

def build_behavior_graph(nodes: List[ActionNode]) -> BehaviorGraphModel:
    """
    Build a sequential behavior dependency graph from action nodes.
    For MVP, we use sequential edges based on code order.
    """
    edges = []
    # Sort by line number just in case
    sorted_nodes = sorted(nodes, key=lambda n: n.line_number)
    
    for i in range(len(sorted_nodes) - 1):
        edges.append({
            "source": sorted_nodes[i].id,
            "target": sorted_nodes[i+1].id
        })
        
    return BehaviorGraphModel(nodes=sorted_nodes, edges=edges)

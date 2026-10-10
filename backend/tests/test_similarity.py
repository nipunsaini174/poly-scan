import pytest
from app.models.schemas import ActionNode, BehaviorGraphModel
from app.analyzer.similarity import calculate_similarity

def test_identical_graphs():
    nodes_a = [
        ActionNode(id=1, action_type="EXEC_SYS_CMD"),
        ActionNode(id=2, action_type="FILE_WRITE")
    ]
    graph_a = BehaviorGraphModel(nodes=nodes_a, edges=[])
    
    nodes_b = [
        ActionNode(id=1, action_type="EXEC_SYS_CMD"),
        ActionNode(id=2, action_type="FILE_WRITE")
    ]
    graph_b = BehaviorGraphModel(nodes=nodes_b, edges=[])
    
    result = calculate_similarity(graph_a, graph_b)
    
    assert result.similarity_percentage == 100.0
    assert result.graph_similarity == 100.0
    assert len(result.matched_actions) == 2
    assert len(result.unique_to_a) == 0
    assert len(result.unique_to_b) == 0

def test_completely_different():
    nodes_a = [ActionNode(id=1, action_type="EXEC_SYS_CMD")]
    graph_a = BehaviorGraphModel(nodes=nodes_a, edges=[])
    
    nodes_b = [ActionNode(id=1, action_type="FILE_WRITE")]
    graph_b = BehaviorGraphModel(nodes=nodes_b, edges=[])
    
    result = calculate_similarity(graph_a, graph_b)
    
    assert result.similarity_percentage == 0.0
    assert result.graph_similarity == 0.0
    assert len(result.matched_actions) == 0
    assert result.unique_to_a == ["EXEC_SYS_CMD"]
    assert result.unique_to_b == ["FILE_WRITE"]

def test_empty_graphs():
    graph_a = BehaviorGraphModel(nodes=[], edges=[])
    graph_b = BehaviorGraphModel(nodes=[], edges=[])
    result = calculate_similarity(graph_a, graph_b)
    assert result.similarity_percentage == 0.0

def test_partial_match_different_order():
    nodes_a = [
        ActionNode(id=1, action_type="EXEC_SYS_CMD"),
        ActionNode(id=2, action_type="FILE_WRITE")
    ]
    graph_a = BehaviorGraphModel(nodes=nodes_a, edges=[])
    
    nodes_b = [
        ActionNode(id=1, action_type="FILE_WRITE"),
        ActionNode(id=2, action_type="EXEC_SYS_CMD")
    ]
    graph_b = BehaviorGraphModel(nodes=nodes_b, edges=[])
    
    result = calculate_similarity(graph_a, graph_b)
    
    # Same actions, so tag similarity is 100%
    assert result.similarity_percentage == 100.0
    # Different order, so sequence similarity shouldn't be 100%
    assert result.graph_similarity == 50.0  # LCS is 1 out of 2

def test_one_empty_graph():
    nodes_a = [ActionNode(id=1, action_type="EXEC_SYS_CMD")]
    graph_a = BehaviorGraphModel(nodes=nodes_a, edges=[])
    
    graph_b = BehaviorGraphModel(nodes=[], edges=[])
    
    result = calculate_similarity(graph_a, graph_b)
    
    assert result.similarity_percentage == 0.0
    assert result.graph_similarity == 0.0
    assert len(result.unique_to_a) == 1
    assert result.unique_to_a[0] == "EXEC_SYS_CMD"
    assert len(result.unique_to_b) == 0

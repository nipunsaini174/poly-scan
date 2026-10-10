import pytest
from app.parsers.python_parser import PythonParser
from app.parsers.javascript_parser import JavaScriptParser
from app.analyzer.behavior_graph import build_behavior_graph
from app.analyzer.similarity import calculate_similarity

def test_cross_language_equivalent_1():
    py_code = 'import os\nos.system("malware.exe")'
    js_code = 'child_process.exec("malware.exe")'
    
    py_nodes = PythonParser().parse(py_code)
    js_nodes = JavaScriptParser().parse(js_code)
    
    py_graph = build_behavior_graph(py_nodes)
    js_graph = build_behavior_graph(js_nodes)
    
    result = calculate_similarity(py_graph, js_graph)
    assert result.similarity_percentage == 100.0
    assert result.graph_similarity == 100.0
    assert result.matched_actions == ['EXEC_SYS_CMD']

def test_cross_language_equivalent_2():
    py_code = 'open("x.txt", "w")'
    js_code = 'fs.writeFileSync("x.txt", "data")'
    
    py_nodes = PythonParser().parse(py_code)
    js_nodes = JavaScriptParser().parse(js_code)
    
    py_graph = build_behavior_graph(py_nodes)
    js_graph = build_behavior_graph(js_nodes)
    
    result = calculate_similarity(py_graph, js_graph)
    assert result.similarity_percentage == 100.0
    assert result.matched_actions == ['FILE_WRITE']

def test_cross_language_different():
    py_code = 'import socket\ns = socket.socket()\ns.connect(("1.1.1.1", 80))'
    js_code = 'child_process.spawn("whoami")'
    
    py_nodes = PythonParser().parse(py_code)
    js_nodes = JavaScriptParser().parse(js_code)
    
    py_graph = build_behavior_graph(py_nodes)
    js_graph = build_behavior_graph(js_nodes)
    
    result = calculate_similarity(py_graph, js_graph)
    assert result.similarity_percentage == 0.0
    assert result.graph_similarity == 0.0
    assert result.matched_actions == []
    assert result.unique_to_a == ['NET_OUTBOUND']
    assert result.unique_to_b == ['PROCESS_EXEC']

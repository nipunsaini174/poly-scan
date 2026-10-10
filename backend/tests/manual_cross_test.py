from app.parsers.python_parser import PythonParser
from app.parsers.javascript_parser import JavaScriptParser
from app.analyzer.behavior_graph import build_behavior_graph
from app.analyzer.similarity import calculate_similarity

def run_cross_case(case_num, title, py_code, js_code):
    print(f"\n--- Cross-Language Case {case_num}: {title} ---")
    py_parser = PythonParser()
    js_parser = JavaScriptParser()
    
    py_nodes = py_parser.parse(py_code)
    py_graph = build_behavior_graph(py_nodes)
    py_tags = [n.action_type for n in py_nodes]
    print(f"Python Code Tags: {py_tags}")
    
    js_nodes = js_parser.parse(js_code)
    js_graph = build_behavior_graph(js_nodes)
    js_tags = [n.action_type for n in js_nodes]
    print(f"JavaScript Code Tags: {js_tags}")
    
    sim = calculate_similarity(py_graph, js_graph)
    print(f"Similarity: {sim.similarity_percentage}%")
    print(f"Graph/Sequence Similarity: {sim.graph_similarity}%")
    print(f"Matched: {sim.matched_actions}")
    print(f"Explanation: {sim.explanation}")


case1_py = """
import os
os.system("malware.exe")
"""
case1_js = """
const cp = require('child_process');
cp.exec("malware.exe");
"""
run_cross_case(1, "Command Execution", case1_py, case1_js)

case2_py = """
open("stolen_data.txt", "w")
"""
case2_js = """
const fs = require('fs');
fs.writeFileSync("stolen_data.txt", "data");
"""
run_cross_case(2, "File Write", case2_py, case2_js)

case3_py = """
import base64
import subprocess
payload = base64.b64decode("xyz")
subprocess.Popen(payload)
"""
case3_js = """
const payload = Buffer.from("xyz", "base64");
child_process.spawn(payload);
"""
run_cross_case(3, "Decode Payload + Spawn Process", case3_py, case3_js)


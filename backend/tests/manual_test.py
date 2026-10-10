from app.parsers.python_parser import PythonParser
from app.analyzer.behavior_graph import build_behavior_graph
from app.analyzer.similarity import calculate_similarity

def run_case(case_num, code_a, code_b):
    print(f"\n--- CASE {case_num} ---")
    parser = PythonParser()
    
    nodes_a = parser.parse(code_a)
    graph_a = build_behavior_graph(nodes_a)
    tags_a = [n.action_type for n in nodes_a]
    print(f"Code A Tags: {tags_a}")
    
    nodes_b = parser.parse(code_b)
    graph_b = build_behavior_graph(nodes_b)
    tags_b = [n.action_type for n in nodes_b]
    print(f"Code B Tags: {tags_b}")
    
    sim = calculate_similarity(graph_a, graph_b)
    print(f"Similarity: {sim.similarity_percentage}%")
    print(f"Graph/Sequence Similarity: {sim.graph_similarity}%")
    print(f"Matched: {sim.matched_actions}")
    print(f"Explanation: {sim.explanation}")


case1_a = """
import os
os.system("malware.exe")
open("x.txt", "w")
"""
case1_b = """
import subprocess
subprocess.run(["malware.exe"])
with open("x.txt", "w") as f:
    f.write("test")
"""
run_case(1, case1_a, case1_b)

case2_a = """
import socket
s = socket.socket()
s.connect(('127.0.0.1', 80))
"""
case2_b = """
import socket
s = socket.socket()
s.connect(('10.0.0.1', 443))
"""
run_case(2, case2_a, case2_b)

case3_a = """
import base64, os
payload = base64.b64decode("abc")
os.system(payload)
"""
case3_b = """
import base64, subprocess
payload = base64.b64decode("xyz")
subprocess.Popen(payload)
"""
run_case(3, case3_a, case3_b)

case4_a = """
import math
print(math.sqrt(16))
"""
case4_b = """
import os
os.system("calc.exe")
"""
run_case(4, case4_a, case4_b)

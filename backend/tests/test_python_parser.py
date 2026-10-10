import pytest
from app.parsers.python_parser import PythonParser
from app.analyzer.action_mapper import EXEC_SYS_CMD, FILE_WRITE, NET_OUTBOUND, DECODE_PAYLOAD

def test_parse_system_exec():
    code = "import os\nos.system('calc.exe')"
    parser = PythonParser()
    nodes = parser.parse(code)
    assert len(nodes) == 1
    assert nodes[0].action_type == EXEC_SYS_CMD

def test_parse_file_write():
    code = "open('test.txt', 'w')\nopen('read.txt', 'r')"
    parser = PythonParser()
    nodes = parser.parse(code)
    # Only the write open() should map to FILE_WRITE
    # The read open() maps to FILE_READ
    assert len(nodes) == 2
    assert nodes[0].action_type == FILE_WRITE

def test_parse_network():
    code = "import socket\ns = socket.socket()\ns.connect(('127.0.0.1', 80))"
    parser = PythonParser()
    nodes = parser.parse(code)
    assert len(nodes) == 1
    assert nodes[0].action_type == NET_OUTBOUND

def test_parse_base64_decode():
    code = "import base64\nbase64.b64decode('cGF5bG9hZA==')"
    parser = PythonParser()
    nodes = parser.parse(code)
    assert len(nodes) == 1
    assert nodes[0].action_type == DECODE_PAYLOAD

def test_malformed_input():
    code = "this is not python code"
    parser = PythonParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(code)
    assert "Syntax error in Python code" in str(exc.value)

def test_empty_input():
    parser = PythonParser()
    nodes = parser.parse("")
    assert len(nodes) == 0

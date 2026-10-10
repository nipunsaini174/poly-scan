import pytest
from app.parsers.javascript_parser import JavaScriptParser
from app.analyzer.action_mapper import EXEC_SYS_CMD, PROCESS_EXEC, FILE_WRITE, NET_OUTBOUND, DECODE_PAYLOAD

def test_parse_exec():
    code = "const cp = require('child_process');\ncp.exec('whoami');"
    # Note: Our simple MVP parser expects `child_process.exec` exactly or alias tracking.
    # We will test the direct form for the MVP baseline as requested by user instructions:
    # "child_process.exec() -> EXEC_SYS_CMD"
    code_direct = "child_process.exec('whoami');"
    parser = JavaScriptParser()
    nodes = parser.parse(code_direct)
    assert len(nodes) == 1
    assert nodes[0].action_type == EXEC_SYS_CMD

def test_parse_spawn():
    code_direct = "child_process.spawn('whoami');"
    parser = JavaScriptParser()
    nodes = parser.parse(code_direct)
    assert len(nodes) == 1
    assert nodes[0].action_type == PROCESS_EXEC

def test_parse_file_write():
    code = "fs.writeFileSync('test.txt', 'data');\nfs.createWriteStream('out.txt');"
    parser = JavaScriptParser()
    nodes = parser.parse(code)
    assert len(nodes) == 2
    assert nodes[0].action_type == FILE_WRITE
    assert nodes[1].action_type == FILE_WRITE

def test_parse_network():
    code = "net.createConnection({port: 80});"
    parser = JavaScriptParser()
    nodes = parser.parse(code)
    assert len(nodes) == 1
    assert nodes[0].action_type == NET_OUTBOUND

def test_parse_base64_decode():
    code = "Buffer.from('cGF5bG9hZA==', 'base64');"
    parser = JavaScriptParser()
    nodes = parser.parse(code)
    assert len(nodes) == 1
    assert nodes[0].action_type == DECODE_PAYLOAD

def test_malformed_input():
    code = "this is not valid js () => {"
    parser = JavaScriptParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(code)
    assert "Syntax error in JavaScript code" in str(exc.value)

def test_empty_input():
    parser = JavaScriptParser()
    nodes = parser.parse("")
    assert len(nodes) == 0

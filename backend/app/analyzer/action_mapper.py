# Action tags definition
EXEC_SYS_CMD = "EXEC_SYS_CMD"
PROCESS_EXEC = "PROCESS_EXEC"
FILE_WRITE = "FILE_WRITE"
NET_OUTBOUND = "NET_OUTBOUND"
DECODE_PAYLOAD = "DECODE_PAYLOAD"
FILE_READ = "FILE_READ"
UNKNOWN = "UNKNOWN"

def map_python_action(node_info: dict) -> str:
    """Map python-specific operation details to universal action tags."""
    if node_info.get("type") == "call":
        func_name = node_info.get("func_name", "")
        
        # execution
        if func_name in ["os.system"]:
            return EXEC_SYS_CMD
        if func_name.startswith("subprocess."):
            return PROCESS_EXEC
            
        # file ops
        if func_name == "open":
            args = node_info.get("args", [])
            # check if write mode
            if len(args) > 1 and any(m in args[1] for m in ["w", "a", "x", "+"]):
                return FILE_WRITE
            return FILE_READ
            
        # network
        if func_name.endswith(".connect") or "socket.connect" in func_name:
            return NET_OUTBOUND
            
        # decoding
        if func_name in ["base64.b64decode"]:
            return DECODE_PAYLOAD
            
    return UNKNOWN

def map_javascript_action(node_info: dict) -> str:
    """Map javascript-specific operation details to universal action tags."""
    if node_info.get("type") == "call":
        func_name = node_info.get("func_name", "")
        
        # execution
        if func_name in ["child_process.exec"] or func_name.endswith(".exec"):
            return EXEC_SYS_CMD
        if func_name in ["child_process.spawn"] or func_name.endswith(".spawn"):
            return PROCESS_EXEC
            
        # file ops
        if func_name in ["fs.writeFileSync", "fs.createWriteStream"]:
            return FILE_WRITE
            
        # network
        if func_name in ["net.createConnection"] or func_name.endswith(".connect"):
            return NET_OUTBOUND
            
        # decoding
        if func_name in ["Buffer.from"]:
            args = node_info.get("args", [])
            if len(args) > 1 and args[1] == "base64":
                return DECODE_PAYLOAD
                
    return UNKNOWN

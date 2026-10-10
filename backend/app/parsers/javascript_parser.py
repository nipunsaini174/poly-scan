import esprima
from typing import List
from app.parsers.base import BaseParser
from app.models.schemas import ActionNode
from app.analyzer.action_mapper import map_javascript_action, UNKNOWN

class JavaScriptParser(BaseParser):
    def __init__(self):
        self.nodes = []
        self.current_id = 1
        
    def _get_full_name(self, node):
        if node.type == 'Identifier':
            return node.name
        elif node.type == 'MemberExpression':
            obj = self._get_full_name(node.object)
            prop = self._get_full_name(node.property)
            if obj and prop:
                return f"{obj}.{prop}"
            elif prop:
                return prop
        return None
        
    def _get_arg_value(self, arg):
        if arg.type == 'Literal':
            return str(arg.value)
        return "<expr>"

    def _traverse(self, node):
        if not node or not hasattr(node, "type"):
            return
            
        if node.type == 'CallExpression':
            func_name = self._get_full_name(node.callee)
            if func_name:
                args = [self._get_arg_value(arg) for arg in getattr(node, 'arguments', [])]
                
                node_info = {
                    "type": "call",
                    "func_name": func_name,
                    "args": args
                }
                
                action_type = map_javascript_action(node_info)
                if action_type != UNKNOWN:
                    line_no = node.loc.start.line if hasattr(node, 'loc') and node.loc else -1
                    self.nodes.append(ActionNode(
                        id=self.current_id,
                        action_type=action_type,
                        details=node_info,
                        original_code=func_name, # Simplified for MVP
                        line_number=line_no
                    ))
                    self.current_id += 1
                    
        # recursively traverse all keys that might hold children
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, "type"):
                        self._traverse(item)
            elif hasattr(value, "type"):
                self._traverse(value)

    def parse(self, source_code: str) -> List[ActionNode]:
        self.nodes = []
        self.current_id = 1
        try:
            tree = esprima.parseScript(source_code, {"loc": True})
            self._traverse(tree)
            return sorted(self.nodes, key=lambda x: x.line_number)
        except Exception as e:
            raise ValueError(f"Syntax error in JavaScript code: {str(e)}")

import ast
from typing import List
from app.parsers.base import BaseParser
from app.models.schemas import ActionNode
from app.analyzer.action_mapper import map_python_action, UNKNOWN

class PythonAstVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []
        self.current_id = 1

    def _get_full_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_full_name(node.value)
            if value:
                return f"{value}.{node.attr}"
            return node.attr
        return None

    def visit_Call(self, node):
        func_name = self._get_full_name(node.func)
        if func_name:
            args = []
            for arg in node.args:
                if isinstance(arg, ast.Constant):
                    args.append(str(arg.value))
                else:
                    args.append("<expr>")
                    
            node_info = {
                "type": "call",
                "func_name": func_name,
                "args": args
            }
            
            action_type = map_python_action(node_info)
            if action_type != UNKNOWN:
                self.nodes.append(ActionNode(
                    id=self.current_id,
                    action_type=action_type,
                    details=node_info,
                    original_code=ast.unparse(node) if hasattr(ast, "unparse") else "",
                    line_number=node.lineno
                ))
                self.current_id += 1
                
        self.generic_visit(node)


class PythonParser(BaseParser):
    def parse(self, source_code: str) -> List[ActionNode]:
        try:
            tree = ast.parse(source_code)
            visitor = PythonAstVisitor()
            visitor.visit(tree)
            return visitor.nodes
        except SyntaxError as e:
            raise ValueError(f"Syntax error in Python code: {str(e)}")

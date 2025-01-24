import ast
from typing import List
from .base_parser import BaseParser

class PythonParser(BaseParser):
    """
    Parse Python files to extract dependencies (import statements).
    """

    def parse(self, content: str) -> List[str]:
        tree = ast.parse(content)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        return imports

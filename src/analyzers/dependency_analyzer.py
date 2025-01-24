from typing import Dict, List
import networkx as nx
from networkx.readwrite import json_graph  
from .parsers.language_parsers import PythonParser, DotNetParser, JavaScriptParser, CppParser, JavaParser

class DependencyAnalyzer:
    """
    Analyze dependencies for multi-language repositories.
    """

    PARSERS = {
        ".py": PythonParser(),
        ".cs": DotNetParser(),
        ".js": JavaScriptParser(),
        ".ts": JavaScriptParser(),
        ".cpp": CppParser(),
        ".h": CppParser(),
        ".java": JavaParser(),
    }

    def __init__(self, files: Dict[str, str]):
        """
        Initialize the DependencyAnalyzer with a dictionary of files and their content.
        
        Args:
            files (Dict[str, str]): A dictionary where keys are file paths and values are file contents.
        """
        self.files = files
        self.graph = nx.DiGraph()

    def analyze(self):
        """
        Analyze dependencies and build a dependency graph.
        """
        for file_path, content in self.files.items():
            ext = f".{file_path.split('.')[-1]}"
            parser = self.PARSERS.get(ext)
            if parser:
                try:
                    dependencies = parser.parse(content)
                    for dep in dependencies:
                        self.graph.add_edge(file_path, dep)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")

    def export_graph(self, format: str = "json") -> str:
        """
        Export the dependency graph in the desired format.
        
        Args:
            format (str): The export format. Currently supports "json".

        Returns:
            str: The exported graph as a string in the chosen format.

        Raises:
            ValueError: If an unsupported format is provided.
        """
        if format == "json":
            return json_graph.node_link_data(self.graph)
        raise ValueError(f"Unsupported format: {format}")

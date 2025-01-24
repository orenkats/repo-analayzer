from typing import Dict, List
import networkx as nx # type: ignore
from .parsers import python_parser, dotnet_parser, javascript_parser, cpp_parser

class DependencyAnalyzer:
    """
    Analyze dependencies for multi-language repositories.
    """

    PARSERS = {
        ".py": python_parser.PythonParser(),
        ".cs": dotnet_parser.DotNetParser(),
        ".js": javascript_parser.JavaScriptParser(),
        ".ts": javascript_parser.JavaScriptParser(),
        ".cpp": cpp_parser.CppParser(),
        ".h": cpp_parser.CppParser(),
    }

    def __init__(self, files: Dict[str, str]):
        """
        Initialize the DependencyAnalyzer with a dictionary of files and their content.
        """
        self.files = files
        self.graph = nx.DiGraph()

    def analyze(self):
        """
        Analyze dependencies and build a dependency graph.
        """
        for file_path, content in self.files.items():
            ext = file_path.split(".")[-1]
            parser = self.PARSERS.get(f".{ext}")
            if parser:
                dependencies = parser.parse(content)
                for dep in dependencies:
                    self.graph.add_edge(file_path, dep)

    def export_graph(self, format: str = "json") -> str:
        """
        Export the dependency graph.
        """
        if format == "json":
            return nx.node_link_data(self.graph)
        raise ValueError(f"Unsupported format: {format}")

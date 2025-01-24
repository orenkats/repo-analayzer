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
        ".tsx": JavaScriptParser(),
        ".cpp": CppParser(),
        ".h": CppParser(),
        ".java": JavaParser(),
    }

    def __init__(self, files: Dict[str, str], valid_files: List[str]):
        """
        Initialize the DependencyAnalyzer with a dictionary of files and valid files.

        Args:
            files (Dict[str, str]): A dictionary of file paths and their content.
            valid_files (List[str]): A list of valid file paths in the repository.
        """
        self.files = files
        self.valid_files = valid_files
        self.graph = nx.DiGraph()

        # Create a mapping of valid namespaces or file stems for matching
        self.namespace_mapping = self._build_namespace_mapping()

    def _build_namespace_mapping(self) -> Dict[str, str]:
        """
        Build a mapping from logical namespaces to file paths.

        Returns:
            Dict[str, str]: A dictionary mapping logical namespaces to file paths.
        """
        namespace_map = {}
        for file_path in self.valid_files:
            parts = file_path.replace("/", ".").split(".")
            file_name = parts[-2]  # Extract file name without extension
            namespace = ".".join(parts[:-1])  # Use full path as namespace

            # Add direct mappings
            namespace_map[file_name] = file_path
            namespace_map[namespace] = file_path

            # Support simplified names (e.g., ServiceName.Entities)
            for i in range(len(parts) - 1):
                simplified_namespace = ".".join(parts[i:])
                namespace_map[simplified_namespace] = file_path

        return namespace_map

    def analyze(self):
        """
        Analyze dependencies and build a dependency graph.
        """
        print("Starting dependency analysis...")
        for file_path, content in self.files.items():
            ext = f".{file_path.split('.')[-1]}"
            parser = self.PARSERS.get(ext)
            if not parser:
                print(f"Skipping unsupported file: {file_path}")
                continue

            try:
                print(f"Parsing dependencies for: {file_path}")
                dependencies = parser.parse(content)
                print(f"Dependencies found in {file_path}: {dependencies}")

                mapped_deps = [
                    self._resolve_dependency(dep) for dep in dependencies
                ]
                mapped_deps = [dep for dep in mapped_deps if dep and dep != "EXTERNAL"]

                if not mapped_deps:
                    print(f"No mapped dependencies found for {file_path}. Skipping.")
                else:
                    print(f"Mapped dependencies for {file_path}: {mapped_deps}")

                for dep in mapped_deps:
                    self.graph.add_edge(file_path, dep)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")


    def _resolve_dependency(self, dependency: str) -> str:
        """
        Resolve a dependency to a file path using the namespace mapping.

        Args:
            dependency (str): The dependency to resolve.

        Returns:
            str: The resolved file path or None if no match is found.
        """
        # Attempt exact match
        if dependency in self.namespace_mapping:
            return self.namespace_mapping[dependency]

        # Fuzzy match: Check if any namespace ends with the dependency
        for namespace, file_path in self.namespace_mapping.items():
            if namespace.endswith(dependency):
                return file_path

        # Fuzzy match: Check if the dependency maps to a directory structure
        for namespace, file_path in self.namespace_mapping.items():
            if dependency.replace(".", "/") in file_path:
                return file_path

        print(f"Unresolved dependency: {dependency}")
        return None

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
            return json_graph.node_link_data(self.graph, edges="links")
        raise ValueError(f"Unsupported format: {format}")

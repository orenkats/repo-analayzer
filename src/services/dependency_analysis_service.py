import os
import json
from typing import Dict, List
import networkx as nx
from networkx.readwrite import json_graph
from infrastructure.redis_client import RedisClient
from utils.file_utils import save_text_to_file, read_text_from_file
from utils.parsing_utils import PythonParser, DotNetParser, JavaScriptParser, CppParser, JavaParser


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
        self.raw_dependencies = {}      # Stores raw dependencies from parsers
        self.resolved_dependencies = {} # Stores resolved dependencies after mapping
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
        Parse dependencies for all files and resolve them into a unified structure.
        """
        print("Starting dependency analysis...")

        # Step 1: Parse raw dependencies for all files
        self._parse_dependencies()

        # Step 2: Resolve raw dependencies into actual file paths
        self.resolve_dependencies()

        # Step 3: Build the dependency graph
        self.build_graph()

    def _parse_dependencies(self):
        """
        Parse raw dependencies for all files using appropriate parsers.
        """
        for file_path, content in self.files.items():
            ext = f".{file_path.split('.')[-1]}"
            parser = self.PARSERS.get(ext)
            if not parser:
                print(f"Skipping unsupported file: {file_path}")
                continue

            try:
                print(f"Parsing dependencies for: {file_path}")
                self.raw_dependencies[file_path] = parser.parse(content)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
                self.raw_dependencies[file_path] = []

    def resolve_dependencies(self):
        """
        Resolve raw dependencies into actual file paths using namespace mapping.
        """
        print("Resolving dependencies...")

        for file_path, dependencies in self.raw_dependencies.items():
            resolved = []

            for dependency in dependencies:
                resolved_path = self._resolve_dependency(dependency)
                if resolved_path:
                    resolved.append(resolved_path)
                else:
                    print(f"Unresolved dependency in {file_path}: {dependency}")

            self.resolved_dependencies[file_path] = resolved

    def _resolve_dependency(self, dependency: str) -> str:
        """
        Resolve a dependency to a file path using precomputed mappings and fuzzy matching.

        Args:
            dependency (str): The raw dependency string.

        Returns:
            str: The resolved file path or None if not found.
        """
        # Attempt exact match
        if dependency in self.namespace_mapping:
            return self.namespace_mapping[dependency]

        # Fuzzy matching using difflib
        from difflib import get_close_matches
        candidates = get_close_matches(dependency, self.namespace_mapping.keys())
        if candidates:
            return self.namespace_mapping[candidates[0]]

        # No match found
        return None

    def build_graph(self):
        """
        Build the dependency graph using resolved dependencies.
        """
        print("Building dependency graph...")
        for file_path, resolved_deps in self.resolved_dependencies.items():
            for dep in resolved_deps:
                self.graph.add_edge(file_path, dep)

    def export_graph(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Export the dependency graph in a readable JSON format.

        Returns:
            Dict[str, Dict[str, List[str]]]: A structured representation of dependencies.
        """
        output = {}

        for node in self.graph.nodes:
            # Collect outgoing edges (dependencies)
            depends_on = list(self.graph.successors(node))
            
            # Collect incoming edges (files using this file)
            used_by = list(self.graph.predecessors(node))
            
            # Build the structured output
            output[node] = {"Depends On": depends_on}
            if used_by:
                output[node]["Used By"] = used_by

        return output


async def analyze_and_export_dependencies(files: dict, valid_files: list, repo_id: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Analyze dependencies and store the dependency graph in Redis.

    Args:
        files (dict): Dictionary of file paths and their content.
        valid_files (list): List of valid file paths.
        repo_id (str): Unique identifier for the repository.

    Returns:
        dict: The dependency graph.
    """
    print("Analyzing dependencies...")
    analyzer = DependencyAnalyzer(files, valid_files)
    analyzer.analyze()

    dependency_graph = analyzer.export_graph()

    # Save to Redis
    redis_client = RedisClient()
    redis_client.set_data(f"dependency_map:{repo_id}", dependency_graph)

    print(f"Dependency graph saved to Redis under 'dependency_map:{repo_id}'.")
    return dependency_graph
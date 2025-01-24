from src.analyzers.dependency_analyzer import DependencyAnalyzer
from src.utils.file_utils import save_text_to_file
import os
import json


async def analyze_and_export_dependencies(files: dict, valid_files: list, output_path: str) -> None:
    """
    Analyze dependencies and export the dependency graph.

    Args:
        files (dict): Dictionary of file paths and their content.
        valid_files (list): List of valid file paths.
        output_path (str): Path to save the dependency graph.
    """
    print("Analyzing dependencies...")
    analyzer = DependencyAnalyzer(files, valid_files)
    analyzer.analyze()

    print("Exporting dependency graph...")
    dependency_graph = analyzer.export_graph()
    os.makedirs(output_path, exist_ok=True)
    save_text_to_file(json.dumps(dependency_graph, indent=2), os.path.join(output_path, "dependency_graph.json"))
    print(f"Dependency graph saved to '{output_path}/dependency_graph.json'")

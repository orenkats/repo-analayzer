import pytest
from src.analyzers.dependency_analyzer import DependencyAnalyzer

@pytest.fixture
def sample_files():
    """
    Fixture providing a dictionary of sample files and their content.
    """
    return {
        "file1.py": "import os\nimport sys",
        "file2.js": "import React from 'react';\nimport './App.css';",
        "file3.cs": "using System;\nusing System.Collections.Generic;",
    }

def test_dependency_analyzer_initialization(sample_files):
    """
    Test initializing the DependencyAnalyzer.
    """
    analyzer = DependencyAnalyzer(sample_files)
    assert analyzer.files == sample_files
    assert len(analyzer.graph.nodes) == 0

def test_analyze_dependencies(sample_files):
    """
    Test analyzing dependencies and building the dependency graph.
    """
    analyzer = DependencyAnalyzer(sample_files)
    analyzer.analyze()

    # Check if the graph contains nodes for all files
    assert set(analyzer.graph.nodes) == set(sample_files.keys())

    # Check dependencies for Python file
    python_deps = list(analyzer.graph.successors("file1.py"))
    assert "os" in python_deps
    assert "sys" in python_deps

def test_export_graph(sample_files):
    """
    Test exporting the dependency graph to JSON format.
    """
    analyzer = DependencyAnalyzer(sample_files)
    analyzer.analyze()
    exported_graph = analyzer.export_graph(format="json")

    assert isinstance(exported_graph, dict)
    assert "nodes" in exported_graph
    assert "links" in exported_graph

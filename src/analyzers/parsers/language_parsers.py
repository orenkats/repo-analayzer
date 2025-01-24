import re
from typing import List
from .base_parser import BaseParser


class PythonParser(BaseParser):
    """
    Parse Python files to extract dependencies (imports).
    """

    def parse(self, file_content: str) -> List[str]:
        """
        Parse Python file content to extract dependencies.

        Args:
            file_content (str): Content of the Python file.

        Returns:
            List[str]: List of imported modules.
        """
        import ast

        tree = ast.parse(file_content)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports


class DotNetParser(BaseParser):
    """
    Parse .NET C# files to extract dependencies (using statements).
    """

    def parse(self, file_content: str) -> List[str]:
        """
        Parse .NET C# file content to extract dependencies.

        Args:
            file_content (str): Content of the C# file.

        Returns:
            List[str]: List of dependencies (using namespaces).
        """
        dependencies = []
        for line in file_content.splitlines():
            match = re.match(r"^\s*using\s+([\w.]+);", line)
            if match:
                dependencies.append(match.group(1))
        return dependencies


class JavaScriptParser(BaseParser):
    """
    Parse JavaScript/TypeScript files to extract dependencies (import statements).
    """

    def parse(self, file_content: str) -> List[str]:
        """
        Parse JavaScript/TypeScript file content to extract dependencies.

        Args:
            file_content (str): Content of the JavaScript/TypeScript file.

        Returns:
            List[str]: List of dependencies.
        """
        dependencies = []
        for line in file_content.splitlines():
            match = re.match(r"^\s*import\s+.*\s+from\s+['\"](.+)['\"]", line)
            if match:
                dependencies.append(match.group(1))
        return dependencies


class JavaParser(BaseParser):
    """
    Parse Java files to extract dependencies (import statements).
    """

    def parse(self, file_content: str) -> List[str]:
        """
        Parse Java file content to extract dependencies.

        Args:
            file_content (str): Content of the Java file.

        Returns:
            List[str]: List of dependencies (import statements).
        """
        dependencies = []
        for line in file_content.splitlines():
            match = re.match(r"^\s*import\s+([\w.]+);", line)
            if match:
                dependencies.append(match.group(1))
        return dependencies


class CppParser(BaseParser):
    """
    Parse C++ files to extract dependencies (#include directives).
    """

    def parse(self, file_content: str) -> List[str]:
        """
        Parse C++ file content to extract dependencies.

        Args:
            file_content (str): Content of the C++ file.

        Returns:
            List[str]: List of dependencies (#include directives).
        """
        dependencies = []
        for line in file_content.splitlines():
            match = re.match(r'^\s*#include\s+[<"]([^">]+)[">]', line)
            if match:
                dependencies.append(match.group(1))
        return dependencies

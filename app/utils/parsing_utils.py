from abc import ABC, abstractmethod
from typing import List
import re
import ast

class BaseParser(ABC):
    """
    Abstract base class for all parsers.
    """

    @abstractmethod
    def parse(self, file_content: str) -> List[str]:
        """
        Parse a file's content and extract dependencies.

        Args:
            file_content (str): Content of the file as a string.

        Returns:
            List[str]: A list of dependencies.
        """
        pass


class PythonParser(BaseParser):
    """
    Parse Python files to extract dependencies (imports).
    """

    def parse(self, file_content: str) -> List[str]:
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
        dependencies = []
        for line in file_content.splitlines():
            match = re.match(r'^\s*#include\s+[<"]([^">]+)[">]', line)
            if match:
                dependencies.append(match.group(1))
        return dependencies

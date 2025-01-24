import re
from typing import List
from .base_parser import BaseParser

class JavaParser(BaseParser):
    """
    Parse Java files to extract dependencies (import statements).
    """

    def parse(self, content: str) -> List[str]:
        """
        Parse the content of a Java file and return a list of dependencies.
        Args:
            content (str): The content of the Java file.
        Returns:
            List[str]: List of dependencies (import statements).
        """
        return re.findall(r"^\s*import\s+([\w.]+);", content, re.MULTILINE)

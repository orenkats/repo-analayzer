import re
from typing import List
from .base_parser import BaseParser

class DotNetParser(BaseParser):
    """
    Parse .NET files to extract dependencies (using statements).
    """

    def parse(self, content: str) -> List[str]:
        return re.findall(r"^\s*using\s+([\w.]+);", content, re.MULTILINE)

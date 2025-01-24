import re
from typing import List
from .base_parser import BaseParser

class JavaScriptParser(BaseParser):
    """
    Parse JavaScript/TypeScript files to extract dependencies (import statements).
    """

    def parse(self, content: str) -> List[str]:
        return re.findall(r"^\s*import\s+.*\s+from\s+['\"](.+)['\"]", content, re.MULTILINE)

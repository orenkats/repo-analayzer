import re
from typing import List
from .base_parser import BaseParser

class CppParser(BaseParser):
    """
    Parse C++ files to extract dependencies (#include directives).
    """

    def parse(self, content: str) -> List[str]:
        return re.findall(r'^\s*#include\s+[<"]([^">]+)[">]', content, re.MULTILINE)

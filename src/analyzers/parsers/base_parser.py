from abc import ABC, abstractmethod
from typing import List

class BaseParser(ABC):
    """
    Abstract base class for dependency parsers.
    """

    @abstractmethod
    def parse(self, content: str) -> List[str]:
        """
        Parse the content of a file and return a list of dependencies.
        """
        pass

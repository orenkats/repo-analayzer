from abc import ABC, abstractmethod
from typing import List


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

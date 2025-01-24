import os
from typing import List

def save_text_to_file(content: str, file_path: str) -> None:
    """
    Save text content to a file.

    Args:
        content (str): The text content to save.
        file_path (str): The path to the file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def read_text_from_file(file_path: str) -> str:
    """
    Read text content from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The text content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def list_files_in_directory(directory: str) -> List[str]:
    """
    List all files in a directory recursively.

    Args:
        directory (str): The directory to scan.

    Returns:
        List[str]: A list of file paths.
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

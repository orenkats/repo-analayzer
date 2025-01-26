import os
import shutil
from typing import Dict
from utils.file_utils import save_text_to_file


class RepositoryService:
    def __init__(self, base_dir: str):
        """
        Initialize the RepositoryService with a base directory.

        Args:
            base_dir (str): The base directory where repository files will be stored.
        """
        self.base_dir = base_dir

    def save_repository_files(self, files: Dict[str, str]) -> None:
        """
        Save repository files to the local file system.

        Args:
            files (Dict[str, str]): Dictionary of file paths and their content.
        """
        for file_path, content in files.items():
            # Construct the full path for the file
            full_path = os.path.join(self.base_dir, file_path)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Save the file content
            save_text_to_file(content, full_path)

        print(f"Repository files have been saved to {self.base_dir}")

    def cleanup(self) -> None:
        """
        Clean up the temporary directory.
        """
        shutil.rmtree(self.base_dir, ignore_errors=True)
        print(f"Temporary directory {self.base_dir} has been cleaned up.")

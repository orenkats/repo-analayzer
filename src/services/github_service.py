from typing import List, Dict
import asyncio
from src.infrastructure.github_client import GitHubClient


class GitHubService:
    """
    A service to interact with GitHub repositories.
    """

    def __init__(self, client: GitHubClient):
        """
        Initialize the GitHubService with a GitHubClient.
        """
        self.client = client

    async def fetch_repo_tree(self, owner: str, repo: str, branch: str = "main") -> List[Dict]:
        url = f"{self.client.BASE_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        response = await self.client.get(url)
        return response.get("tree", [])  # Ensure only the "tree" key is returned


    async def fetch_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> str:
        """
        Fetch the content of a specific file in the repository.
        """
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        return await self.client.fetch_raw(url)

    async def fetch_all_file_contents(self, owner: str, repo: str, file_paths: List[str], branch: str = "main") -> Dict[str, str]:
        """
        Fetch contents of all files concurrently.

        Args:
            owner (str): Repository owner.
            repo (str): Repository name.
            file_paths (List[str]): List of file paths to fetch.
            branch (str): Branch to fetch from.

        Returns:
            Dict[str, str]: A dictionary where keys are file paths and values are file contents.
        """
        async def fetch_content(path):
            try:
                return path, await self.fetch_file_content(owner, repo, path, branch)
            except Exception as e:
                print(f"Failed to fetch {path}: {e}")
                return path, None

        tasks = [fetch_content(path) for path in file_paths]
        results = await asyncio.gather(*tasks)
        return {path: content for path, content in results if content}

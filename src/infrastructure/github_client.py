import aiohttp
import asyncio
from typing import List, Dict


class GitHubClient:
    """
    A client to interact with GitHub's API for fetching repositories and their contents using asyncio.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str):
        """
        Initialize the GitHubClient with a personal access token.
        """
        self.headers = {"Authorization": f"token {token}"} if token else {}

    async def fetch_repo_tree(self, owner: str, repo: str, branch: str = "main") -> List[Dict]:
        """
        Fetch the complete tree of a GitHub repository asynchronously.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("tree", [])

    async def fetch_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> str:
        """
        Fetch the content of a specific file in the repository asynchronously.
        """
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()

    async def fetch_all_file_contents(
        self, owner: str, repo: str, file_paths: List[str], branch: str = "main"
    ) -> Dict[str, str]:
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

        # Only keep successfully fetched files
        return {path: content for path, content in results if content}

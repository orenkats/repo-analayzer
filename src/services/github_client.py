import requests
from typing import Optional

class GitHubClient:
    """
    A client to interact with GitHub's API for fetching repositories and their contents.
    """
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHubClient with an optional personal access token.
        """
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def fetch_repo_tree(self, owner: str, repo: str, branch: str = "main") -> list:
        """
        Fetch the complete tree of a GitHub repository.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("tree", [])

    def fetch_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> str:
        """
        Fetch the content of a specific file in the repository.
        """
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

from typing import Dict
from urllib.parse import urlparse

def parse_git_url(url: str) -> Dict[str, str]:
    """
    Parse a GitHub repository URL into its components.

    Args:
        url (str): The GitHub repository URL.

    Returns:
        Dict[str, str]: A dictionary containing the owner, repo name, and branch (if provided).

    Raises:
        ValueError: If the URL is invalid.
    """
    if "github.com" not in url:
        raise ValueError("Invalid GitHub URL")

    parsed_url = urlparse(url)
    parts = parsed_url.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("URL does not contain enough parts to identify the repo")

    owner, repo = parts[0], parts[1]

    # Check for optional branch in the URL
    branch = "main"  # Default to "main"
    if len(parts) > 3 and parts[2] == "tree":
        branch = parts[3]

    if repo.endswith(".git"):
        repo = repo[:-4]

    return {"owner": owner, "repo": repo, "branch": branch}


def is_valid_git_url(url: str) -> bool:
    """
    Validate if a URL is a GitHub repository.

    Args:
        url (str): The GitHub URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    parts = url.split("/")
    return (
        url.startswith("https://github.com/")
        and len(parts) >= 5
        and all(parts[i] for i in [3, 4])  # Ensure owner and repo are not empty
    )

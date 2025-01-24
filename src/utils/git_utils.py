from typing import List

def parse_git_url(url: str) -> dict:
    """
    Parse a GitHub repository URL into its components.

    Args:
        url (str): The GitHub repository URL.

    Returns:
        dict: A dictionary containing the owner and repo name.
    """
    if "github.com" not in url:
        raise ValueError("Invalid GitHub URL")

    parts = url.split("/")
    if len(parts) < 5:
        raise ValueError("URL does not contain enough parts to identify the repo")

    owner, repo = parts[-2], parts[-1]
    if repo.endswith(".git"):
        repo = repo[:-4]

    return {"owner": owner, "repo": repo}


def is_valid_git_url(url: str) -> bool:
    """
    Validate if a URL is a GitHub repository.

    Args:
        url (str): The GitHub URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    return url.startswith("https://github.com/") and len(url.split("/")) >= 5

import pytest
import requests
from unittest.mock import patch
from src.services.github_client import GitHubClient

@pytest.fixture
def github_client():
    """
    Fixture providing a GitHubClient instance.
    """
    return GitHubClient(token="dummy_token")

@patch("src.services.github_client.requests.get")
def test_fetch_repo_tree(mock_get, github_client):
    """
    Test fetching the repository tree.
    """
    mock_response = {
        "tree": [{"path": "file1.py", "type": "blob"}, {"path": "dir1/file2.js", "type": "blob"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    tree = github_client.fetch_repo_tree(owner="dummy_owner", repo="dummy_repo")
    assert len(tree) == 2
    assert tree[0]["path"] == "file1.py"

@patch("src.services.github_client.requests.get")
def test_fetch_file_content(mock_get, github_client):
    """
    Test fetching file content from a GitHub repository.
    """
    mock_content = "print('Hello, World!')"
    mock_get.return_value.text = mock_content
    mock_get.return_value.status_code = 200

    content = github_client.fetch_file_content(owner="dummy_owner", repo="dummy_repo", path="file1.py")
    assert content == mock_content



async def fetch_repository_data(github_client, owner: str, repo: str, branch: str) -> tuple:
    """
    Fetch the repository tree and file contents.

    Args:
        github_client (GitHubClient): GitHub client instance.
        owner (str): Repository owner.
        repo (str): Repository name.
        branch (str): Branch name.

    Returns:
        tuple: Valid files and their content.
    """
    print(f"Fetching repository tree for {owner}/{repo} (branch: {branch})...")
    repo_tree = await github_client.fetch_repo_tree(owner, repo, branch=branch)
    valid_files = [item["path"] for item in repo_tree if item["type"] == "blob"]
    print(f"Repository tree fetched: {len(valid_files)} valid files identified.")

    print("Fetching file contents asynchronously...")
    files = await github_client.fetch_all_file_contents(owner, repo, valid_files, branch)
    print(f"Fetched contents for {len(files)} files.")
    return valid_files, files

import asyncio
from config.env_loader import load_environment, get_github_token
from .integrations.github_client import GitHubClient
from .services.github_service import fetch_repository_data
from .services.dependency_service import analyze_and_export_dependencies
from .utils.filtering import filter_source_files
from .utils.git_utils import parse_git_url
from config.settings import SOURCE_EXTENSIONS


async def main():
    """
    Entry point of the application.
    """
    try:
        # Load environment variables
        await load_environment()

        print("Welcome to Repo Analyzer!")

        # Input: GitHub repository URL
        repo_url = input("Enter the GitHub repository URL: ").strip()

        # Parse repository information
        repo_info = parse_git_url(repo_url)
        owner, repo, branch = repo_info["owner"], repo_info["repo"], repo_info["branch"]

        # Get GitHub token
        token = get_github_token()

        # Initialize GitHubClient
        github_client = GitHubClient(token=token)

        # Fetch repository data
        valid_files, files = await fetch_repository_data(github_client, owner, repo, branch)

        # Filter source files
        filtered_files, filtered_valid_files = filter_source_files(files, valid_files, SOURCE_EXTENSIONS)

        # Analyze dependencies and export results
        await analyze_and_export_dependencies(filtered_files, filtered_valid_files, output_path="output")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

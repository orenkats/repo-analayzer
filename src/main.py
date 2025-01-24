from src.services.github_client import GitHubClient
from src.analyzers.dependency_analyzer import DependencyAnalyzer
from src.utils.file_utils import save_text_to_file
from src.utils.git_utils import parse_git_url
from dotenv import load_dotenv
import os
import json


def main():
    """
    Entry point of the application.
    """
    # Load environment variables explicitly
    dotenv_path = os.path.abspath(".env")
    if not os.path.exists(dotenv_path):
        print(f"Error: .env file not found at {dotenv_path}")
        return
    load_dotenv(dotenv_path)

    print("Welcome to Repo Analyzer!")

    # Input: GitHub repository URL
    repo_url = input("Enter the GitHub repository URL: ").strip()

    try:
        # Parse the repository URL
        repo_info = parse_git_url(repo_url)
        owner, repo, branch = repo_info["owner"], repo_info["repo"], repo_info["branch"]
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Get GitHub token from environment variables
    token = os.getenv("GITHUB_API_TOKEN")
    if not token:
        print("Error: GitHub token not found. Please set it in the .env file.")
        return

    # Initialize GitHub client
    github_client = GitHubClient(token=token)

    try:
        # Fetch the repository tree
        print(f"Fetching repository tree for {owner}/{repo} (branch: {branch})...")
        repo_tree = github_client.fetch_repo_tree(owner, repo, branch=branch)
        file_paths = [item['path'] for item in repo_tree if item['type'] == "blob"]

        # Fetch content of all files and store in a dictionary
        print("Fetching file contents...")
        files = {}
        for file_path in file_paths:
            print(f"Fetching content for: {file_path}")
            files[file_path] = github_client.fetch_file_content(owner, repo, file_path, branch)

        # Analyze dependencies
        print("Analyzing dependencies...")
        analyzer = DependencyAnalyzer(files)
        analyzer.analyze()

        # Export the dependency graph
        print("Exporting dependency graph...")
        dependency_graph_json = analyzer.export_graph(format="json")
        os.makedirs("output", exist_ok=True)  # Ensure the output directory exists
        save_text_to_file(json.dumps(dependency_graph_json, indent=2), "output/dependency_graph.json")

        print("Dependency graph saved to 'output/dependency_graph.json'")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

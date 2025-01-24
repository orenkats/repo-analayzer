from src.services.github_client import GitHubClient
from src.analyzers.dependency_analyzer import DependencyAnalyzer
from src.utils.file_utils import save_text_to_file
from src.utils.git_utils import parse_git_url

def main():
    """
    Entry point of the application.
    """
    print("Welcome to Repo Analyzer!")

    # Input: GitHub repository URL
    repo_url = input("Enter the GitHub repository URL: ").strip()
    
    try:
        repo_info = parse_git_url(repo_url)
        owner, repo = repo_info["owner"], repo_info["repo"]
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Initialize GitHub client
    github_client = GitHubClient(token="YOUR_GITHUB_TOKEN")

    try:
        # Fetch repository contents
        contents = github_client.fetch_repo_contents(owner, repo)
        file_paths = [item['path'] for item in contents if item['type'] == "file"]

        # Analyze dependencies
        analyzer = DependencyAnalyzer(file_paths)
        analyzer.analyze()

        # Generate and save results
        dependency_graph_text = analyzer.get_dependency_graph_text()
        save_text_to_file(dependency_graph_text, "output/dependency_graph.txt")
        print("Dependency graph saved to 'output/dependency_graph.txt'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

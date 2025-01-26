import asyncio
from config.env_loader import load_environment, get_github_token
from src.infrastructure.github_client import GitHubClient
from src.infrastructure.redis_client import RedisClient
from src.services.redis_service import RedisService
from src.services.github_service import GitHubService
from src.services.dependency_analysis_service import analyze_and_export_dependencies
from src.services.bundling_service import BundleService
from src.utils.filtering import filter_source_files
from src.utils.git_utils import parse_git_url
from config.settings import SOURCE_EXTENSIONS


async def main():
    """
    Entry point of the application.
    """
    # Load environment variables
    await load_environment()
    print("Welcome to Repo Analyzer!")

    # Input: GitHub repository URL
    repo_url = input("Enter the GitHub repository URL: ").strip()
    repo_info = parse_git_url(repo_url)
    owner, repo, branch = repo_info["owner"], repo_info["repo"], repo_info["branch"]

    # Initialize services
    token = get_github_token()
    github_client = GitHubClient(token)
    redis_client = RedisClient()
    redis_service = RedisService(redis_client)
    github_service = GitHubService(github_client)

    # Fetch repository data
    print("Fetching repository data...")
    repo_tree = await github_service.fetch_repo_tree(owner, repo, branch)
    valid_files = [item["path"] for item in repo_tree if item["type"] == "blob"]
    files = await github_service.fetch_all_file_contents(owner, repo, valid_files, branch)

    # Save file content to Redis using RedisService
    repo_id = f"{owner}_{repo}"
    for file_path, content in files.items():
        redis_service.save_file_content(repo_id, file_path, content)

    # Filter source files
    filtered_files, filtered_valid_files = filter_source_files(files, valid_files, SOURCE_EXTENSIONS)

    # Analyze dependencies and save to Redis using RedisService
    dependency_graph = await analyze_and_export_dependencies(filtered_files, filtered_valid_files, repo_id)
    redis_service.save_dependency_map(repo_id, dependency_graph)

    # On-demand bundle generation (simulating user interaction)
    print("Dependency map generated. You can now generate bundles on demand.")
    while True:
        target_file = input("Enter the target file to generate its bundle (or 'exit' to quit): ").strip()
        if target_file.lower() == "exit":
            break

        bundling_service = BundleService(repo_id, redis_client)
        try:
            bundle_metadata = bundling_service.generate_bundle_for_ui(target_file)
            print(f"\nBundle for {target_file} includes {len(bundle_metadata['related_files'])} files.")
            for file, content in bundle_metadata["file_contents"].items():
                print(f"\nFile: {file}\nContent Preview:\n{content[:500]}...")  # Print the first 500 characters
        except ValueError as e:
            print(f"Error: {e}")

    # Close GitHub client session to avoid unclosed session warnings
    await github_client.close()


if __name__ == "__main__":
    asyncio.run(main())

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, HttpUrl
from app.services.github_service import GitHubService
from app.services.redis_service import RedisService
from app.services.dependency_analysis_service import analyze_and_export_dependencies
from app.utils.filtering import filter_source_files
from app.utils.git_utils import parse_git_url
from app.config.settings import SOURCE_EXTENSIONS

router = APIRouter()


class RepoRequest(BaseModel):
    repo_url: HttpUrl


@router.post("/load-repo")
async def load_repository(repo_request: RepoRequest, request: Request):
    """
    Load a repository, fetch its data, analyze dependencies, and save them to Redis.

    Args:
        repo_request (RepoRequest): The request body containing the repository URL.
        request (Request): The request object to access app state.

    Returns:
        dict: A message indicating success or an error.
    """
    try:
        # Extract the repository URL
        repo_url = str(repo_request.repo_url)

        # Parse repository details
        repo_info = parse_git_url(repo_url)
        owner, repo, branch = repo_info["owner"], repo_info["repo"], repo_info["branch"]
        repo_id = f"{owner}_{repo}"

        # Access shared clients from app state
        github_client = request.app.state.github_client
        redis_client = request.app.state.redis_client

        # Initialize services using shared clients
        github_service = GitHubService(github_client)
        redis_service = RedisService(redis_client)

        # Fetch repository data
        print("Fetching repository tree...")
        repo_tree = await github_service.fetch_repo_tree(owner, repo, branch)
        valid_files = [item["path"] for item in repo_tree if item["type"] == "blob"]
        print(f"Valid files identified: {len(valid_files)}")

        print("Fetching file contents...")
        files = await github_service.fetch_all_file_contents(owner, repo, valid_files, branch)
        print(f"Fetched contents for {len(files)} files.")

        # Save file content to Redis
        print("Saving file content to Redis...")
        for file_path, content in files.items():
            redis_service.save_file_content(repo_id, file_path, content)

        # Filter source files
        print("Filtering source files...")
        filtered_files, filtered_valid_files = filter_source_files(files, valid_files, SOURCE_EXTENSIONS)

        # Analyze and save dependency map
        print("Analyzing dependencies...")
        dependency_graph = await analyze_and_export_dependencies(filtered_files, filtered_valid_files, repo_id)
        print("Saving dependency map to Redis...")
        redis_service.save_dependency_map(repo_id, dependency_graph)

        return {"message": "Repository loaded and dependency map generated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

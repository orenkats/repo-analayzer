from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import repo, bundle
from app.config.env_loader import load_environment,get_github_token
from app.infrastructure.github_client import GitHubClient
from app.infrastructure.redis_client import RedisClient
import sys


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing environment...")
    await load_environment()
    print("Environment loaded.")

    token = get_github_token()
    print(f"GitHub Token: {token}")

    app.state.github_client = GitHubClient(token)
    app.state.redis_client = RedisClient()

    print("Resources initialized.")
    yield
    print("Cleaning up resources...")

    await app.state.github_client.close()
    print("GitHubClient session closed.")


app = FastAPI(title="Repo Analyzer", lifespan=lifespan)

# Include routes
app.include_router(repo.router, prefix="/api/repo", tags=["Repository"])
app.include_router(bundle.router, prefix="/api/bundle", tags=["Bundle"])

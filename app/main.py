from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import repo, bundle
from app.config.env_loader import load_environment, get_github_token
from app.infrastructure.github_client import GitHubClient
from app.infrastructure.redis_client import RedisClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def initialize_resources():
    """
    Initialize shared resources like GitHubClient and RedisClient.
    """
    await load_environment()
    logger.info("Environment variables loaded.")
    token = get_github_token()
    logger.info("GitHub token retrieved.")
    github_client = GitHubClient(token)
    redis_client = RedisClient()
    return github_client, redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context for managing app startup and shutdown.
    """
    logger.info("Initializing resources...")
    github_client, redis_client = await initialize_resources()

    # Attach resources to app state
    app.state.github_client = github_client
    app.state.redis_client = redis_client
    logger.info("Resources initialized successfully.")

    yield

    # Cleanup resources
    await app.state.github_client.close()
    logger.info("GitHubClient session closed.")
    logger.info("App shutdown complete.")


app = FastAPI(title="Repo Analyzer", lifespan=lifespan)

# Include routes
app.include_router(repo.router, prefix="/api/repo", tags=["Repository"])
app.include_router(bundle.router, prefix="/api/bundle", tags=["Bundle"])

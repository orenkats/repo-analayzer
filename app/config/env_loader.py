import os
from dotenv import load_dotenv


async def load_environment() -> None:
    """
    Load environment variables from a .env file.
    """
    dotenv_path = os.path.abspath(".env")
    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f".env file not found at {dotenv_path}")
    load_dotenv(dotenv_path)


def get_github_token() -> str:
    """
    Retrieve the GitHub API token from environment variables.
    """
    token = os.getenv("GITHUB_API_TOKEN")
    if not token:
        raise ValueError("GitHub token not found. Please set it in the .env file.")
    return token

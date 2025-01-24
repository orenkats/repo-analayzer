import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application settings and configurations.
    """
    GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")
    OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY", "output")

settings = Settings()

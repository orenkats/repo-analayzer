from dotenv import load_dotenv
import os

# Load .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

# Read environment variables
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")

if not GITHUB_API_TOKEN:
    raise ValueError("GitHub token not found. Please set it in the .env file.")

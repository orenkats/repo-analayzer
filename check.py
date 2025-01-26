import os
import sys

print("Current Working Directory:", os.getcwd())
print("Python Path:", sys.path)

try:
    from app.main import app
    print("FastAPI app imported successfully.")
except Exception as e:
    print("Error importing FastAPI app:", e)

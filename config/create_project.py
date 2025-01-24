import os

# Define the folder and file structure
structure = {
    "repo-analyzer": {
        "src": {
            "analyzers": {
                "parsers": {
                    "python_parser.py": "",
                    "dotnet_parser.py": "",
                    "javascript_parser.py": "",
                    "cpp_parser.py": "",
                    "java_parser.py": ""
                },
                "dependency_analyzer.py": ""
            },
            "generators": {
                "prompt_generator.py": ""
            },
            "integrations": {
                "openai_client.py": ""
            },
            "services": {
                "github_client.py": ""
            },
            "utils": {
                "git_utils.py": "",
                "file_utils.py": ""
            },
            "main.py": ""
        },
        "tests": {
            "test_analyzers.py": "",
            "test_parsers.py": "",
            "test_services.py": ""
        },
        "config": {
            "settings.py": ""
        },
        "requirements.txt": "",
        "README.md": "",
        ".gitignore": "",
        ".env": "",
        "docker-compose.yml": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)  # Create directories
            create_structure(path, content)  # Recursively create subdirectories and files
        else:
            with open(path, "w") as f:  # Create empty files
                f.write(content)  # Optionally write initial content

# Create the project structure
create_structure(".", structure)

print("Project structure created successfully!")

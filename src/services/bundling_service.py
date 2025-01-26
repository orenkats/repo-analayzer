from typing import Dict, List
from src.infrastructure.redis_client import RedisClient

class BundleService:
    def __init__(self, repo_id: str, redis_client: RedisClient):
        """
        Initialize the BundleService with a repository ID and Redis client.
        """
        self.repo_id = repo_id
        self.redis_client = redis_client

    def get_all_related_files(self, dependency_graph: Dict[str, Dict[str, List[str]]], target_file: str) -> set:
        """
        Get all related files (Depends On + Used By) for the target file.
        """
        if target_file not in dependency_graph:
            raise ValueError(f"Target file {target_file} not found in the dependency graph.")

        related_files = set()
        queue = [target_file]

        while queue:
            current_file = queue.pop(0)
            if current_file in dependency_graph:
                depends_on = dependency_graph[current_file].get("Depends On", [])
                used_by = dependency_graph[current_file].get("Used By", [])
                all_related = depends_on + used_by

                for related_file in all_related:
                    if related_file not in related_files:
                        queue.append(related_file)

                related_files.update(all_related)

        return related_files

    def generate_bundle(self, target_file: str) -> Dict[str, str]:
        """
        Generate a bundle for the target file using the dependency graph from Redis.
        """
        # Fetch the dependency map from Redis
        dependency_graph = self.redis_client.get_data(f"dependency_map:{self.repo_id}")
        if not dependency_graph:
            raise ValueError(f"Dependency map for repo '{self.repo_id}' not found in Redis.")

        # Get all related files for the target file
        related_files = self.get_all_related_files(dependency_graph, target_file)
        related_files.add(target_file)

        # Fetch file contents for the bundle
        bundle = {}
        for file in sorted(related_files):
            file_content = self.redis_client.get_data(f"file_content:{self.repo_id}:{file}")
            bundle[file] = file_content if file_content else f"Error: Content for {file} not found."

        return bundle

    def generate_bundle_for_ui(self, target_file: str) -> Dict[str, Dict[str, str]]:
        """
        Generate a bundle with metadata for UI display, including file content and related files.
        """
        bundle = self.generate_bundle(target_file)
        metadata = {
            "target_file": target_file,
            "related_files": list(bundle.keys()),
            "file_contents": bundle,
        }
        return metadata

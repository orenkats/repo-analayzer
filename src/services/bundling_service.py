from typing import Dict, List
from infrastructure.redis_client import RedisClient

class BundleService:
    def __init__(self, repo_id: str):
        """
        Initialize the BundleService with a repository ID.
        """
        self.repo_id = repo_id
        self.redis_client = RedisClient()

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

    def generate_bundle(self, target_file: str):
        """
        Generate a bundle for the target file using the dependency graph from Redis.
        """
        dependency_graph = self.redis_client.get_data(f"dependency_map:{self.repo_id}")
        if not dependency_graph:
            raise ValueError(f"Dependency map for repo '{self.repo_id}' not found in Redis.")

        related_files = self.get_all_related_files(dependency_graph, target_file)
        related_files.add(target_file)

        bundle = {}
        for file in sorted(related_files):
            file_content = self.redis_client.get_data(f"file_content:{self.repo_id}:{file}")
            bundle[file] = file_content if file_content else f"Error: Content for {file} not found."

        return bundle

    def generate_all_bundles(self):
        """
        Generate bundles for all files in the repository.
        """
        dependency_graph = self.redis_client.get_data(f"dependency_map:{self.repo_id}")
        if not dependency_graph:
            raise ValueError(f"Dependency map for repo '{self.repo_id}' not found in Redis.")

        for target_file in dependency_graph.keys():
            bundle = self.generate_bundle(target_file)
            print(f"Bundle generated for {target_file}: {len(bundle)} files included.")

from app.infrastructure.redis_client import RedisClient

class RedisService:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    def save_file_content(self, repo_id: str, file_path: str, content: str):
        self.redis_client.set_data(f"file_content:{repo_id}:{file_path}", content)

    def save_dependency_map(self, repo_id: str, dependency_map: dict):
        self.redis_client.set_data(f"dependency_map:{repo_id}", dependency_map)

    def get_dependency_map(self, repo_id: str):
        return self.redis_client.get_data(f"dependency_map:{repo_id}")

    def get_file_content(self, repo_id: str, file_path: str):
        return self.redis_client.get_data(f"file_content:{repo_id}:{file_path}")

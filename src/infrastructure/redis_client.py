import redis
import json
import os

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        """
        Initialize the Redis client.
        """
        self.client = redis.StrictRedis(
            host=host, port=port, db=db, decode_responses=True
        )

    def set_data(self, key: str, value: dict):
        """
        Store data in Redis as JSON.
        """
        self.client.set(key, json.dumps(value))

    def get_data(self, key: str):
        """
        Retrieve data from Redis and parse it as JSON.
        """
        data = self.client.get(key)
        return json.loads(data) if data else None

    def delete_data(self, key: str):
        """
        Delete data from Redis by key.
        """
        self.client.delete(key)

    def flush_db(self):
        """
        Clear the entire Redis database.
        """
        self.client.flushdb()
        print("Redis database flushed.")

import redis
import pickle

class RedisCache:
    def __init__(self, host='localhost', port=6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def get(self, key):
        """
        Get the value stored in the cache for the given key.
        Returns None if key is not found.
        """
        return self.redis_client.get(key)

    def set(self, key, value, expire_time=None):
        """
        Set the value in the cache for the given key.
        If expire_time is provided (in seconds), the key will automatically expire after that time.
        """

        self.redis_client.set(key, value, ex=expire_time)

    def delete(self, key):
        """
        Delete the value stored in the cache for the given key.
        """
        self.redis_client.delete(key)


cache = RedisCache()

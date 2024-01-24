
"""Module that does different things with a Redis client connection."""

import redis
import uuid
from typing import Union, ByteString


class Cache:
    """Represents cache system using Redis."""

    def __init__(self):
        """Initialises cache and stores an instance of the Redis client."""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, ByteString, int, float]) -> str:
        """Generates a random key and persists the <data> into Redis.
        
        Arg:
            data: the value to store in Redis.

        Returns:
            the key as a str."""

        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

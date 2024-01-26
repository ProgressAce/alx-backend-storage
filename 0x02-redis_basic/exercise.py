#!/usr/bin/env python3
"""Module that does different things with a Redis client connection."""

import redis
import uuid
from typing import Any, Callable, Optional, Union


def count_calls(self, method: Callable[[None], None]) -> Callable[[None], None]:
    """Counts the number of times a method was called."""
    key = method.__qualname__
    self._redis.set(key, 0)  # key for counting a method's call count

    @functools.wraps(method)
    def wrapper(*args):
        """Performs the count incrementally."""
        self._redis.incr(key)

        return method(args)

    return wrapper

class Cache:
    """Represents cache system using Redis."""

    def __init__(self):
        """Initialises cache and stores an instance of the Redis client."""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key and persists the <data> into Redis.

        Arg:
            data: the value to store in Redis.

        Returns:
            the key as a str."""

        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str,
            fn: Optional[Callable[[ByteString], Any]]=None) -> Any:
        """Gets the value of a key in its desired Python format.

        Args:
            key: the key to look for in Redis.
            fn: a function used to convert the found value to its
            desirable format.

        Returns:
            The value in its desirable format, instead of as a byte.
            Same with Redis, if key not found then None is returned."""

        value = self._redis.get(key)
        if value is None:
            return None

        if fn is None:
            return value

        desired_value = fn(value)
        return desired_value

    def get_str(self, key: str) -> str:
        """Provides <Cache.get> with the correct function for str conversion.

        Args:
            key: the key to pass to <self.get>

        Returns:
            a str value from <self.get>
        """

        value = self.get(key, lambda val: val.decode("utf-8"))
        return value

    def get_int(self, key: str) -> int:
        """Provides <Cache.get> with the correct function for int conversion.

        Arg:
            key: the key to pass to <self.get>.

        Returns:
            an int value from <self.get>
        """

        value = self.get(key, int)
        return value

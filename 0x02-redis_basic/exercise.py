#!/usr/bin/env python3
"""Module that does different things with a Redis client connection."""

import redis
import uuid
from functools import wraps
from typing import Any, Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    """Counts the number of times a method was called."""
    key: str = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Performs the count incrementally."""
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Records the input and output history of a method using Redis."""
    in_key: str = method.__qualname__ + ":inputs"
    out_key: str = method.__qualname__ + ":outputs"

    @wraps(method)
    def record_history(self, *args):  # kwargs are ignored for this exercise
        """Adds the input args and output results of a method to lists.

        They are either added to the list for inputs or for outputs.
        These lists are stored in the local redis client server."""

        for arg in args:
            if type(arg) in [str, bytes, int]:
                self._redis.rpush(in_key, arg)

        method_output = method(self, *args)
        self._redis.rpush(out_key, method_output)

        return method_output

    return record_history


class Cache:
    """Represents cache system using Redis."""

    def __init__(self):
        """Initialises cache and stores an instance of the Redis client."""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
            fn: Optional[Callable[[bytes], Any]] = None) -> Any:
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

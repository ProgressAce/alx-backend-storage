#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache


print("\n----Exercise 1----\n")
cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

del cache


print("\n----Exercise 2----\n")
cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    print(fn)
    assert cache.get(key, fn=fn) == value
assert cache.get('yoyo') == None  # key does not exist

k1 = cache.store("yo")
assert cache.get_str(k1) == "yo"
assert cache.get_str("cabbage") == None  # key does not exist

k2 = cache.store("8")
assert cache.get_int(k2) == 8
assert cache.get_int("cabbage") == None  # key does not exist

del cache


print("\n----Exercise 3----\n")
cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))

del cache


print("\n----Exercise 4----\n")
cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

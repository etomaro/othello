from functools import lru_cache

@lru_cache()
def memo2(n):
    for i in range(100000):
        n += 1
    return n
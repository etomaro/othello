"""
関数のメモ化のテスト
"""
from functools import lru_cache
import time
from memo2 import memo2


@lru_cache()
def memo(n):
    for i in range(100000):
        n += 1
    return n


def test(n):
    for i in range(100000):
        n += 1
    return n

if __name__ == "__main__":
    n = 1
    start_time = time.time()
    for i in range(100):
        result = test(n)
    print("普通のメソッド\n")
    print(time.time() - start_time)

    print("\n")

    n = 1
    start_time = time.time()
    for i in range(100):
        result = memo2(n)
    print("memoメソッド\n")
    print(time.time() - start_time)

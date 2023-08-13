"""
関数のメモ化のテスト
"""
from functools import lru_cache
import time
from memo2 import memo2

class Test():
    @lru_cache()
    def memo(self, n):
        for i in range(100000):
            n += 1
        return n

    def test(self, n):
        for i in range(100000):
            n += 1
        return n
    
    def action(self):
        for i in range(100):
            result = self.test(1)
        
    def action2(self):
        for i in range(100):
            result = self.memo(1)


if __name__ == "__main__":
    test = Test()
    start_time = time.time()
    test.action()
    print("普通のメソッド\n")
    print(time.time() - start_time)

    print("\n")

    test = Test()
    start_time = time.time()
    test.action2()
    print("memoメソッド\n")
    print(time.time() - start_time)

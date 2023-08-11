"""
インスタンスメソッドと普通のメソッドの速度比較
"""
import time

class Test():
    def __init__(self):
        self.num = 0
    
    def count(self):
        self.num += 1


def nomarl_method(count):
    count += 1
    return count


if __name__ == "__main__":
    test = Test()
    start_time = time.time()
    for i in range(100000):
        test.count()
    print("インスタンスメソッド\n")
    print(time.time() - start_time)

    print("\n")

    count = 0
    start_time = time.time()
    for i in range(100000):
        count = nomarl_method(count)
    print("普通のメソッド\n")
    print(time.time() - start_time)
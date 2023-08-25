import concurrent.futures
import time
"""
ProcessPoolExecutorを使ったサンプルコード
"""
import psutil


def func(i):
    return i * 2

if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=psutil.cpu_count()) as executor:
        rets = executor.map(func, range(10))
        for ret in rets:
            print(ret)

# print([x for x in rets])
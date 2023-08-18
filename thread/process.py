import concurrent.futures
import time
"""
ProcessPoolExecutorを使ったサンプルコード
"""
from concurrent import futures


def func(i):
    time.sleep(2)
    return i * 2


with futures.ProcessPoolExecutor() as executor:
    rets = executor.map(func, range(10))
    for ret in rets:
        print(ret)

# print([x for x in rets])
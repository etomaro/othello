"""
再起処理(recursive processing)
"""

def total(n):
    """
    1 - nまでの合計を計算する
    """
    if n == 0:
        return 0
    else:
        return n + total(n-1)

def double_list(arr):
    """ 
    リストの要素を2倍にする
    """ 
    if len(arr) == 0:
        return []
    first = arr.pop(0)
    return [first * 2] + double_list(arr)
    


if __name__ == "__main__":
    print(total(10))
    print(double_list([1,2,3,4,5]))
import concurrent.futures


def my_function(arg, arg2):
    """
    何かしらの処理を行う関数
    """
    return arg * arg2, arg + arg2
# ThreadPoolExecutor の場合
with concurrent.futures.ThreadPoolExecutor() as executor:
    # 関数に渡す引数のリスト
    args = [1, 2, 3, 4, 5]
    args2 = [1, 2, 3, 4, 5]

    # map() を使って関数を並行実行し、結果を受け取る
    results = executor.map(my_function, args, args2)

    for result in results:
        a = result[0]
        b = result[1]
        print("a:", a)
        print("b:", b)
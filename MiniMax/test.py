import copy

class Test1():
    def __init__(self):
        self.value = 1

test = Test1()
test2 = copy.deepcopy(test)
test2.value = 2
print(test.value)
print(test2.value)
"""
木の作成
木の探索
    深さ優先探索(DFS)
        行きがけ順(preorder)
        通りがけ順(inorder)
        帰りがけ順(postorder)
    幅優先探索(BFS)
"""


import random



class Node():
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None 


class BST():
    """
    Binary Search Tree(二分木)
    """
    def __init__(self, data_list):
        self.root = None
        self.node = None

        for data in data_list:
            self.insert(data)
    
    def insert(self, data):
        if self.root == None:
            self.root = Node(data)
            self.node = Node(data)
        else:
            node = self.root
            while True:
                if data == node.data:
                    continue
                elif data < node.data:
                    if node.left == None:
                        node.left = Node(data)
                        return
                    else:
                        node = node.left
                        continue
                elif data > node.data:
                    if node.right == None:
                        node.right = Node(data)
                        return
                    else:
                        node = node.right 
                        continue 

    def search(self, data):
        is_find, count = self._dfs_preorder(data)
        if is_find:
            print(f"find {data} !\nsearch count: {count}")
        elif is_find == None:
            print(f"tree is not exist")
        else:
            print(f"not find {data} !\nsearch count: {count}")
                

    def _dfs_preorder(self, data):
        """
        DFS(Deep First Search) > 行きがけ順(preorder)
        1. 木が存在しない場合はNoneを返却
        2. 現時点のNodeの値を調べる
        3. 右、左の順番でNodeが存在しているか調べる。存在している場合はListに追加
        4. Listの最後のオブジェクトを取ってきて値が一致するか調べる
        """
        node = self.root
        if node.data == None:
            return None 

        list = []
        list.append(node)
        
        count = 0
        while len(list) > 0:
            count += 1
            node = list.pop()
            if node.data == data:
                return True, count
            if node.right != None:
                list.append(node.right)
            if node.left != None:
                list.append(node.left)
        
        return False, count


arr = [9, 8, 2, 5, 0, 3, 1, 4, 7, 6]
# random.shuffle(arr)
print(arr)

# #テスト----------------------------------------------------
tree = BST(arr) #配列から二分探索木生成し、treeに代入
tree.search(3)#１０がtreeに存在するか検索


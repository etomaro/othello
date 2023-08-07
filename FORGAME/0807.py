import sys
import math
import numpy as np
import copy
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

CORNERS = ['a1', 'a8', 'h1', 'h8']
EDGES = [
    'a2','a3','a4','a5','a6','a7',
    'b1','b8','c1','c8','d1','d8','e1','e8','f1','f8','g1','g8',
    'h2','h3','h4','h5','h6','h7'
    ]

# -------------------------function-------------------------
class Game():
    def __init__(self, game_info=None):
        """         
        """
        if game_info is not None:
            self.board = game_info["board"]
            self.action_player_id = game_info["action_player_id"]
            self.is_game_over = game_info["is_game_over"]
            self.win_player = game_info["win_player"]
            self.turn = game_info["turn"]
            self.black_count = game_info["black_count"]
            self.white_count = game_info["white_count"]
        else:
            self.board = [[ "." for j in range(8)] for i in range(8)]  # ボードの初期化(後攻(白): 0, 先行(黒): 1, 空き: .)
            self.board[3][3] = "0"
            self.board[4][4] = "0"
            self.board[3][4] = "1"
            self.board[4][3] = "1"
            self.action_player_id = "1"  # "1": 先行(黒)、"0": 後攻(白)
            self.is_game_over = False
            self.win_player = ""  # "1": 先行(黒)の勝ち、"0": 後攻(白)の勝ち、"2": 引き分け
            self.turn = 0  # ターン数
            self.black_count = 2
            self.white_count = 2        

    def step(self, action, player_id):
        """ 
        アクション

        Return:
            next_player_id: 次アクション可能なプレイヤーのID
            actionables: 次アクション可能なリスト
            is_game_over: ゲームが終了したかどうか
        """
        # アクション可能か
        if not self.is_actionable(action, player_id):
            raise Exception("不正なアクションです")

        # アクションを実行
        self.set_board(action, player_id)
        self.set_stone_count()
        self.turn += 1

        # ゲームが終了かどうか
        is_game_over = self.check_game_over()
        if is_game_over:
            return "", [], True

        # 次のアクション可能なプレイヤーを更新
        self.set_next_action_player()

        # 次アクション可能なリストを取得
        actionables = self.get_actionables(self.action_player_id)

        return self.action_player_id, actionables, False

    def set_board(self, action, player_id):
        """
        ボードの更新
        """
        opponent_player_id = "0" if player_id=="1" else "1"

        self.board[action[0]][action[1]] = player_id

        # 2. 挟める石を挟む
        # 周りの8隅の座標
        frame_places = [[action[0]-1, action[1]-1], [action[0]-1, action[1]], [action[0]-1, action[1]+1], [action[0], action[1]-1], [action[0], action[1]+1], [action[0]+1, action[1]-1], [action[0]+1, action[1]], [action[0]+1, action[1]+1]]
        # 周りの8個に相手の石があるかどうか。ある場合挟めるかどうか判定
        change_places_all = []  # 挟んだすべての石の座標
        for frame_place in frame_places:
            frame_row, frame_col = frame_place
            # ボードの外に出る場合は除外
            if frame_row < 0 or frame_row > 7 or frame_col < 0 or frame_col > 7:
                continue
            # 自分の石がある場合は除外
            if self.board[frame_row][frame_col] == player_id:
                continue
            # 石がない場合は除外
            if self.board[frame_row][frame_col] == ".":
                continue
            # 相手の石がある場合
            change_places = []  # 挟める石の座標
            if self.board[frame_row][frame_col] == opponent_player_id:
                # 挟める石を追加
                change_places.append([frame_row, frame_col])
                # ベクトル(周りの8個の座標 - 相手の石の場所の座標)
                vector = [frame_row - action[0], frame_col - action[1]]
                # 自分の石があるまでループ
                next_row = frame_row + vector[0]
                next_col = frame_col + vector[1]
                while True:
                    # ボードの外に出る場合は除外
                    if next_row < 0 or next_row > 7 or next_col < 0 or next_col > 7:
                        break 
                    # 石が置かれていない場合は除外
                    if self.board[next_row][next_col] == ".":
                        break
                    # 自分の石がある場合は挟める
                    if self.board[next_row][next_col] == player_id:
                        # 挟む
                        for change_place in change_places:
                            change_row, change_col = change_place
                            # stateの更新
                            self.board[change_row][change_col] = player_id

                            # 挟んだ石の座標を追加
                            change_places_all.append([change_row, change_col])
                        break
                    # 相手の石がある場合は次の座標を更新
                    if self.board[next_row][next_col] == opponent_player_id:
                        # 挟める石を追加
                        change_places.append([next_row, next_col])

                        next_row += vector[0]
                        next_col += vector[1]
                        continue
        
    def set_stone_count(self):
        """
        石をカウントしてセット
        """
        black_count = 0
        white_count = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == "1":
                    black_count += 1
                elif self.board[i][j] == "0":
                    white_count += 1
        
        self.black_count = black_count
        self.white_count = white_count


    def set_next_action_player(self):
        """
        次アクションできるプレイヤーを更新
        """
        next_player_id = "0" if self.action_player_id=="1" else "1"
        actionables = self.get_actionables(next_player_id)
        if len(actionables) == 0:
            pass 
        else:
            self.action_player_id = next_player_id

    
    def get_actionables(self, player_id):
        """
        可能なアクションを返却

        処理:
          1. 石が置かれていない場所を取得
          2. 1で取得した座標に石を置くことができるか判定
             周りの8隅に相手の石が存在するか
             存在する場合、そのベクトル上で相手の石を挟めるかどうか
        """
        
        # 1. 石が置かれていない場所を取得
        empty_places = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == ".":
                    empty_places.append([i, j])
        
        # 2. 石を置くことができるか判定
        actionables = []
        opponent_player_id = "0" if player_id=="1" else "1"
        for empty_place in empty_places:
            row, col = empty_place
            # 周りの8隅の座標
            frame_places = [[row-1, col-1], [row-1, col], [row-1, col+1], [row, col-1], [row, col+1], [row+1, col-1], [row+1, col], [row+1, col+1]]
            # 周りの8個に相手の石があるかどうか。ある場合挟めるかどうか判定
            for frame_place in frame_places:
                frame_row, frame_col = frame_place
                # ボードの外に出る場合は除外
                if frame_row < 0 or frame_row > 7 or frame_col < 0 or frame_col > 7:
                    continue
                # アクションをするプレイヤーの石がある場合は除外
                if self.board[frame_row][frame_col] == player_id:
                    continue
                # 石がない場合は除外
                if self.board[frame_row][frame_col] == ".":
                    continue
                # 相手の石がある場合
                if self.board[frame_row][frame_col] == opponent_player_id:
                    # ベクトル(周りの8個の座標 - 相手の石の場所の座標)
                    vector = [frame_row - row, frame_col - col]
                    # 自分の石があるまでループ
                    next_row = frame_row + vector[0]
                    next_col = frame_col + vector[1]
                    while True:
                        # ボードの外に出る場合は除外
                        if next_row < 0 or next_row > 7 or next_col < 0 or next_col > 7:
                            break 
                        # 石が置かれていない場合は除外
                        if self.board[next_row][next_col] == ".":
                            break
                        # 自分の石がある場合は挟める
                        if self.board[next_row][next_col] == player_id:
                            if empty_place not in actionables:
                                actionables.append(empty_place)
                            break
                        # 相手の石がある場合は次の座標を更新
                        if self.board[next_row][next_col] == opponent_player_id:
                            next_row += vector[0]
                            next_col += vector[1]
                            continue

        return actionables

    def is_actionable(self, action, player_id):
        """
        アクション可能か判定
        """
        # アクション待ちのプレイヤーかどうか
        if self.action_player_id != player_id:
            return False 
        
        # ゲームが終了しているかどうか
        if self.is_game_over:
            return False 

        # 可能なアクションの手かどうか
        actionable_list = self.get_actionables(player_id)
        if action not in actionable_list:
            return False 

        return True
    
    def check_game_over(self):
        """
        ゲームが終了したかどうかを判定
        """
        result = False
        # どちらかの石が0個になった場合
        black_count = 0
        white_count = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == "1":
                    black_count += 1
                elif self.board[i][j] == "0":
                    white_count += 1
        
        if black_count == 0:
            result = True
            self.win_player = "0"
            self.is_game_over = True
        elif white_count == 0:
            result = True
            self.win_player = "1"
            self.is_game_over = True
        
        # 両者ともアクションできない場合
        black_actionables = self.get_actionables("1")
        white_actionables = self.get_actionables("0")
        if len(black_actionables) == 0 and len(white_actionables) == 0:
            result = True
            self.is_game_over = True
            if black_count > white_count:
                self.win_player = "1"
            elif black_count < white_count:
                self.win_player = "0"
            else:
                self.win_player = "2"
        
        return result

class MiniMaxV4Player():
    """
    MINIMAXを導入
      mini_value()の時にαカットを検討
      max2_value()の時にβカットを検討
      mini2_value()の時にαカットを検討
    4手先まで行動(自分と相手が一回ずつ行動)した後の状態で価値を決めて、min(),max()で最適な手を選択する
    評価関数を設定
    """
    def __init__(self, player_id=""):
        # "1": 先行(黒)、"0": 後攻(白)
        if player_id != "":
            self.player_id = player_id

    def action(self, game):
        """
        アクションをする
        """
        actionables = game.get_actionables(self.player_id)
        if len(actionables) == 0:
            raise Exception("アクションできません")
        
        tmp_game = copy.deepcopy(game)
        action = self.choice(tmp_game)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)


        return next_player_id, actionables, is_game_over
    
    def choice(self, game):
        """
        最適な手を選択する
        """
        actionables = game.get_actionables(self.player_id)
        if len(actionables) == 0:
            raise Exception("アクションできません")
        
        # 価値が最も高い手を選択する
        max_value = float("-inf")  # マイナス無限
        max_action = None
        for action in actionables:
            next_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = next_game.step(action, self.player_id)

            # ゲームが終了した場合
            if next_is_game_over:
                return action
            
            value = self._min_value(next_game, max_value)

            if value >= max_value:
                max_value = value
                max_action = action
        
        return max_action

    def _min_value(self, game, alfa):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限
        opponent_player_id = "1" if self.player_id == "0" else "0"
        actionables = game.get_actionables(opponent_player_id)
        for action in actionables:
            new_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = new_game.step(action, opponent_player_id)
            
            if next_is_game_over:
                return float("-inf")
            
            # 状態の価値を計算
            value = self._max2_value(new_game, min_value)

            # αカット
            if value < alfa:
                return value

            if value <= min_value:
                min_value = value
        
        return min_value

    def _min2_value(self, game, alfa):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限
        opponent_player_id = "1" if self.player_id == "0" else "0"
        actionables = game.get_actionables(opponent_player_id)
        for action in actionables:
            new_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = new_game.step(action, opponent_player_id)
            
            if next_is_game_over:
                return float("-inf")
            
            # 状態の価値を計算
            value = self._evaluate(new_game)

            # αカット
            if value < alfa:
                return value

            if value <= min_value:
                min_value = value

        return min_value

    def _max2_value(self, game, beta):
        """
        最大値を返す
        """
        
        max_value = float("-inf")  # マイナス無限
        actionables = game.get_actionables(self.player_id)
        for action in actionables:
            new_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = new_game.step(action, self.player_id)
            
            if next_is_game_over:
                return float("inf")
            
            # 状態の価値を計算
            value = self._min2_value(new_game, max_value)

            # βカット
            if value > beta:
                return value

            if value >= max_value:
                max_value = value
        
        return max_value

    def _evaluate(self, game):
        """
        葉ノードの評価値を計算(末端ノード)

        ゲームが終了した場合+10000 or -10000を返す
        評価方法
          + 自分の角の数 * 100
          + 相手の角の数 * -100
          + 自分の端の数 * 10
          + 相手の端の数 * -10
          + 自分の石の数 * 1
          + 相手の石の数 * -1
        """

        black_count = game.black_count
        white_count = game.white_count
        black_corner_count = 0
        white_corner_count = 0
        black_edge_count = 0
        white_edge_count = 0
        result = 0

        # 角の数を計算
        if game.board[0][0] == "1":
            black_corner_count += 1
        elif game.board[0][0] == "0":
            white_corner_count += 1
        if game.board[0][7] == "1":
            black_corner_count += 1
        elif game.board[0][7] == "0":
            white_corner_count += 1
        if game.board[7][0] == "1":
            black_corner_count += 1
        elif game.board[7][0] == "0":
            white_corner_count += 1
        if game.board[7][7] == "1":
            black_corner_count += 1
        elif game.board[7][7] == "0":
            white_corner_count += 1
        
        # 端の数を計算
        edge_list = [
            [0,1], [0,2], [0,3], [0,4], [0,5], [0,6],
            [1,0], [2,0], [3,0], [4,0], [5,0], [6,0],
            [1,7], [2,7], [3,7], [4,7], [5,7], [6,7],
            [7,1], [7,2], [7,3], [7,4], [7,5], [7,6],
        ]
        for edge in edge_list:
            if game.board[edge[0]][edge[1]] == "1":
                black_edge_count += 1
            elif game.board[edge[0]][edge[1]] == "0":
                white_edge_count += 1

        # 評価値を計算
        if self.player_id == "1":
            result += black_count * 1
            result += white_count * -1
            result += black_corner_count * 100
            result += white_corner_count * -100
            result += black_edge_count * 10
            result += white_edge_count * -10
        elif self.player_id == "0":
            result += black_count * -1
            result += white_count * 1
            result += black_corner_count * -100
            result += white_corner_count * 100
            result += black_edge_count * -10
            result += white_edge_count * 10
        
        return result 

# -------------------------/function-------------------------

_id = input()  # id of your player.
board_size = int(input())

# game loop
while True:
    state = []
    for i in range(board_size):
        line = input()  # rows from top to bottom (viewer perspective).
        state.append(line)
    
    action_count = int(input())  # number of legal actions for this turn.

    actionable = []
    for i in range(action_count):
        action = input()  # the action
        actionable.append(action)
    # print("actionable: ", actionable, file=sys.stderr, flush=True)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # boardを変換
    board = []
    for row in state:
        new_row = []
        for i in row:
            new_row.append(i)
        board.append(new_row)
    # print("board: ", board, file=sys.stderr, flush=True)
    # print("type board: ", type(board), file=sys.stderr, flush=True)
    # print("type board[0]: ", type(board[0]), file=sys.stderr, flush=True)
    # print("type board[0][0]: ", type(board[0][0]), file=sys.stderr, flush=True)
    black_count = 0
    white_count = 0
    for row in board:
        for i in row:
            if i == "1":
                black_count += 1
            elif i == "0":
                white_count += 0

    game_info = {
        "board": board,
        "action_player_id": _id,
        "is_game_over": False,
        "win_player": "",
        "turn": 0,
        "black_count": black_count,
        "white_count": white_count
    }
    game = Game(game_info)
    player = MiniMaxV4Player(_id)
    action = player.choice(game)

    # actionを変換
    col = chr(action[1] + 97)
    row = str(action[0] + 1)
    choice_action = col+row



    print("choice_action: ", choice_action, file=sys.stderr, flush=True)
    # a-h1-8
    print(choice_action)

class Game():
    def __init__(self, game_info=None):
        """
        ゲームの初期化
            boardの表記
                0 1 2 3 4 5 6 7 
              0 - - - - - - - -
              1 - - - - - - - -
              2 - - - - - - - -
              3 - - - - - - - -
              4 - - - - - - - -
              5 - - - - - - - -
              6 - - - - - - - -
              7 - - - - - - - -
            
            ※ codingameでの表記
                a b c d e f g h
              1 - - - - - - - -
              2 - - - - - - - -
              3 - - - - - - - -
              4 - - - - - - - -
              5 - - - - - - - -
              6 - - - - - - - -
              7 - - - - - - - -
              8 - - - - - - - -

            boardの保存方法
              -> 2次元配列

            ※ codingameでのboardの保存方法
              -> 1次元配列            
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
            print("ゲームを開始します")
            self.print_board()
            self.black_count = 2
            self.white_count = 2
    
    def print_board(self):
        """
        ボードの状態を出力
        """
        result = ""
        for i in range(8):
            for j in range(8):
                result += self.board[i][j]
                result += " "
            result += "\n"
        
        print(f"---{self.turn}回目---\n{result}\n")

            

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

        self.print_board()

        # ゲームが終了かどうか
        is_game_over = self.check_game_over()
        if is_game_over:
            return None, None, True

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

                    # ここには来ないはず
                    print("error")
        
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

                        # ここには来ないはず
                        print("error")

        return actionables

    def is_actionable(self, action, player_id):
        """
        アクション可能か判定
        """
        # アクション待ちのプレイヤーかどうか
        if self.action_player_id != player_id:
            print("アクション待ちのプレイヤーではありません")
            return False 
        
        # ゲームが終了しているかどうか
        if self.is_game_over:
            print("ゲームは終了しています")
            return False 

        # 可能なアクションの手かどうか
        actionable_list = self.get_actionables(player_id)
        if action not in actionable_list:
            print("不可能なアクションです: ")
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

    def get_result(self):
        """
        ゲームの勝敗を取得
        """
        result = {
            "win_player": "",
            "black_count": 0,
            "white_count": 0
        }

        if self.is_game_over:
            result["win_player"] = self.win_player
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == "1":
                        result["black_count"] += 1
                    elif self.board[i][j] == "0":
                        result["white_count"] += 1
        
        return result



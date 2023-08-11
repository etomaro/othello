import sys
import math

# -------------------------function-------------------------
class Game():
    def __init__(self, game_info=None):
        if game_info is not None:
            self.black_board = game_info["black_board"]
            self.white_board = game_info["white_board"]
            self.action_player_id = game_info["action_player_id"]
            self.is_game_over = game_info["is_game_over"]
            self.win_player = game_info["win_player"]
            self.turn = game_info["turn"]
            self.black_count = game_info["black_count"]
            self.white_count = game_info["white_count"]
        else:
            self.black_board = 0x0000000810000000
            self.white_board = 0x0000001008000000
            self.action_player_id = "1"  # "1": 先行(黒)、"0": 後攻(白)
            self.is_game_over = False
            self.win_player = ""  # "1": 先行(黒)の勝ち、"0": 後攻(白)の勝ち、"2": 引き分け
            self.turn = 0  # ターン数
            # self.print_board()
            self.black_count = 2
            self.white_count = 2

    def step(self, action, player_id):

        # アクションを実行
        self.set_board(action, player_id)

        # 石の数を更新
        
        self.black_count = bin(self.black_board).count("1")
        self.white_count = bin(self.white_board).count("1")

        self.turn += 1

        # ゲームが終了かどうか
        is_game_over = self.check_game_over()
        if is_game_over:
            return "", 0x0, True

        # 次アクション可能なリストを取得
        next_player_id = "0" if self.action_player_id=="1" else "1"
        actionables = self.get_actionables(next_player_id)
        
        # 次のアクション可能なプレイヤーを更新
        if actionables == 0:
            actionables = self.get_actionables(self.action_player_id)
        else:
            self.action_player_id = next_player_id

        return self.action_player_id, actionables, False

    def set_board(self, action, player_id):
        """
        ボードの更新
        """
        mask_lr = 0x7e7e7e7e7e7e7e7e
        mask_ud = 0x00ffffffffffff00
        mask_lu_ru_ld_rd = 0x007e7e7e7e7e7e00

        reverse = 0x0000000000000000

        # 石を置く
        if player_id == "1":
            mask_left = mask_lr & self.white_board  # 左方向
            mask_right = mask_lr & self.white_board
            mask_up = mask_ud & self.white_board
            mask_down = mask_ud & self.white_board
            mask_left_up = mask_lu_ru_ld_rd & self.white_board
            mask_right_up = mask_lu_ru_ld_rd & self.white_board
            mask_left_down = mask_lu_ru_ld_rd & self.white_board
            mask_right_down = mask_lu_ru_ld_rd & self.white_board

            l_rev = (action << 1) & mask_left
            r_rev = (action >> 1) & mask_right
            u_rev = (action << 8) & mask_up
            d_rev = (action >> 8) & mask_down
            lu_rev = (action << 7) & mask_left_up
            ru_rev = (action << 9) & mask_right_up
            ld_rev = (action >> 9) & mask_left_down
            rd_rev = (action >> 7) & mask_right_down

            for i in range(5):
                l_rev |= (l_rev << 1) & mask_left
                r_rev |= (r_rev >> 1) & mask_right
                u_rev |= (u_rev << 8) & mask_up
                d_rev |= (d_rev >> 8) & mask_down
                lu_rev |= (lu_rev << 7) & mask_left_up
                ru_rev |= (ru_rev << 9) & mask_right_up
                ld_rev |= (ld_rev >> 9) & mask_left_down
                rd_rev |= (rd_rev >> 7) & mask_right_down
    
            if (l_rev << 1) & self.black_board != 0:
                reverse |= l_rev
            if (r_rev >> 1) & self.black_board != 0:
                reverse |= r_rev
            if (u_rev << 8) & self.black_board != 0:
                reverse |= u_rev
            if (d_rev >> 8) & self.black_board != 0:
                reverse |= d_rev
            if (lu_rev << 7) & self.black_board != 0:
                reverse |= lu_rev
            if (ru_rev << 9) & self.black_board != 0:
                reverse |= ru_rev
            if (ld_rev >> 9) & self.black_board != 0:
                reverse |= ld_rev
            if (rd_rev >> 7) & self.black_board != 0:
                reverse |= rd_rev

            self.black_board |= (action | reverse)
            self.white_board ^= reverse
        
        elif player_id == "0":
            mask_left = mask_lr & self.black_board  # 左方向
            mask_right = mask_lr & self.black_board
            mask_up = mask_ud & self.black_board
            mask_down = mask_ud & self.black_board
            mask_left_up = mask_lu_ru_ld_rd & self.black_board
            mask_right_up = mask_lu_ru_ld_rd & self.black_board
            mask_left_down = mask_lu_ru_ld_rd & self.black_board
            mask_right_down = mask_lu_ru_ld_rd & self.black_board

            l_rev = (action << 1) & mask_left
            r_rev = (action >> 1) & mask_right
            u_rev = (action << 8) & mask_up
            d_rev = (action >> 8) & mask_down
            lu_rev = (action << 7) & mask_left_up
            ru_rev = (action << 9) & mask_right_up
            ld_rev = (action >> 9) & mask_left_down
            rd_rev = (action >> 7) & mask_right_down

            for i in range(5):
                l_rev |= (l_rev << 1) & mask_left
                r_rev |= (r_rev >> 1) & mask_right
                u_rev |= (u_rev << 8) & mask_up
                d_rev |= (d_rev >> 8) & mask_down
                lu_rev |= (lu_rev << 7) & mask_left_up
                ru_rev |= (ru_rev << 9) & mask_right_up
                ld_rev |= (ld_rev >> 9) & mask_left_down
                rd_rev |= (rd_rev >> 7) & mask_right_down
            
            if (l_rev << 1) & self.white_board != 0:
                reverse |= l_rev
            if (r_rev >> 1) & self.white_board != 0:
                reverse |= r_rev
            if (u_rev << 8) & self.white_board != 0:
                reverse |= u_rev
            if (d_rev >> 8) & self.white_board != 0:
                reverse |= d_rev
            if (lu_rev << 7) & self.white_board != 0:
                reverse |= lu_rev
            if (ru_rev << 9) & self.white_board != 0:
                reverse |= ru_rev
            if (ld_rev >> 9) & self.white_board != 0:
                reverse |= ld_rev
            if (rd_rev >> 7) & self.white_board != 0:
                reverse |= rd_rev

            self.white_board |= (action | reverse)
            self.black_board ^= reverse

    def get_actionables(self, player_id):
        """
        可能なアクションを返却

        処理:
          1. 左方向に対してい置ける場所を取得
          2. 右方向に対してい置ける場所を取得
          3. 上方向に対してい置ける場所を取得
          4. 下方向に対してい置ける場所を取得
          5. 左上方向に対してい置ける場所を取得
          6. 右上方向に対してい置ける場所を取得
          7. 左下方向に対してい置ける場所を取得
          8. 右下方向に対してい置ける場所を取得
        """
        mask_lr = 0x7e7e7e7e7e7e7e7e
        mask_ud = 0x00ffffffffffff00
        mask_lu_ru_ld_rd = 0x007e7e7e7e7e7e00

        # 空白の場所
        blank_board = ~(self.black_board | self.white_board)


        if player_id == "1":
            # 1. 左方向に対してい置ける場所を取得
            white_lr_mask = self.white_board & mask_lr  # 列1-6かつ白の場所
            white_ud_mask = self.white_board & mask_ud
            white_mask_lu_ru_ld_rd = self.white_board & mask_lu_ru_ld_rd

            l_white = (self.black_board << 1) & white_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
            r_white = (self.black_board >> 1) & white_lr_mask
            u_white = (self.black_board << 8) & white_ud_mask
            d_white = (self.black_board >> 8) & white_ud_mask
            lu_white = (self.black_board << 9) & white_mask_lu_ru_ld_rd
            ru_white = (self.black_board << 7) & white_mask_lu_ru_ld_rd
            ld_white = (self.black_board >> 7) & white_mask_lu_ru_ld_rd
            rd_white = (self.black_board >> 9) & white_mask_lu_ru_ld_rd

            for i in range(5):
                l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
                r_white |= (r_white >> 1) & white_lr_mask
                u_white |= (u_white << 8) & white_ud_mask
                d_white |= (d_white >> 8) & white_ud_mask
                lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
                ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
                ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
                rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

            legal_left = (l_white << 1) & blank_board
            legal_right = (r_white >> 1) & blank_board
            legal_up = (u_white << 8) & blank_board
            legal_down = (d_white >> 8) & blank_board
            legal_lu = (lu_white << 9) & blank_board
            legal_ru = (ru_white << 7) & blank_board
            legal_ld = (ld_white >> 7) & blank_board
            legal_rd = (rd_white >> 9) & blank_board
        elif player_id == "0":
            # 1. 左方向に対してい置ける場所を取得
            black_lr_mask = self.black_board & mask_lr  # 列1-6かつ白の場所
            black_ud_mask = self.black_board & mask_ud
            black_mask_lu_ru_ld_rd = self.black_board & mask_lu_ru_ld_rd

            l_black = (self.white_board << 1) & black_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
            r_black = (self.white_board >> 1) & black_lr_mask
            u_black = (self.white_board << 8) & black_ud_mask
            d_black = (self.white_board >> 8) & black_ud_mask
            lu_black = (self.white_board << 9) & black_mask_lu_ru_ld_rd
            ru_black = (self.white_board << 7) & black_mask_lu_ru_ld_rd
            ld_black = (self.white_board >> 7) & black_mask_lu_ru_ld_rd
            rd_black = (self.white_board >> 9) & black_mask_lu_ru_ld_rd

            for i in range(5):
                l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
                r_black |= (r_black >> 1) & black_lr_mask
                u_black |= (u_black << 8) & black_ud_mask
                d_black |= (d_black >> 8) & black_ud_mask
                lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
                ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
                ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
                rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

            legal_left = (l_black << 1) & blank_board
            legal_right = (r_black >> 1) & blank_board
            legal_up = (u_black << 8) & blank_board
            legal_down = (d_black >> 8) & blank_board
            legal_lu = (lu_black << 9) & blank_board
            legal_ru = (ru_black << 7) & blank_board
            legal_ld = (ld_black >> 7) & blank_board
            legal_rd = (rd_black >> 9) & blank_board

        # 9. 1-8の合計
        legal = legal_left | legal_right | legal_up | legal_down | legal_lu | legal_ru | legal_ld | legal_rd

        return legal
    
    def check_game_over(self):
        """
        ゲームが終了したかどうかを判定
        """
        result = False

        # どちらかの石が0個になった場合
        if self.black_count == 0:
            self.win_player = "0"
            self.is_game_over = True
            return True
        elif self.white_count == 0:
            self.win_player = "1"
            self.is_game_over = True
            return True
        
        # 両者ともアクションできない場合
        black_actionables = self.get_actionables("1")
        
        # 光速かのため追加
        if black_actionables != 0:
            return False

        white_actionables = self.get_actionables("0")
        if black_actionables == 0 and white_actionables == 0:
            result = True
            self.is_game_over = True
            if self.black_count > self.white_count:
                self.win_player = "1"
            elif self.black_count < self.white_count:
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
        raw_game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }
        action = self._choice(game)

        # ゲーム情報を元に戻す
        self.setting_game(game, raw_game_info)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        return next_player_id, actionables, is_game_over

    def setting_game(self, game, game_info):
        game.black_board = game_info["black_board"]
        game.white_board = game_info["white_board"]
        game.action_player_id = game_info["action_player_id"]
        game.is_game_over = game_info["is_game_over"]
        game.turn = game_info["turn"]
        game.black_count = game_info["black_count"]
        game.white_count = game_info["white_count"]
    
    def _choice(self, game):
        """
        最適な手を選択する
        """
        actionables = game.get_actionables(self.player_id)
        if actionables == 0:
            raise Exception("アクションできません")
        
        # 価値が最も高い手を選択する
        max_value = float("-inf")  # マイナス無限
        max_action = None

        actionables_list = [1 << i for i in range(actionables.bit_length()) if actionables & (1 << i)]

        search_depth = 1  # 探索深さ

        game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }

        for action in actionables_list:
            self.setting_game(game, game_info)
            next_player_id, next_actionables, next_is_game_over = game.step(action, self.player_id)

            # ゲームが終了した場合
            if next_is_game_over:
                return action
            
            if next_player_id == self.player_id:
                value = self._max_value(game, None, search_depth, next_actionables, next_player_id)
            else:
                value = self._min_value(game, max_value, search_depth, next_actionables, next_player_id)

            if value >= max_value:
                max_value = value
                max_action = action
        
        return max_action

    def _min_value(self, game, alfa, search_depth, actionables, action_player_id):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限

        actionables_list = [1 << i for i in range(actionables.bit_length()) if actionables & (1 << i)]
        
        search_depth += 1

        game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }
    
        for action in actionables_list:
            self.setting_game(game, game_info)
            next_player_id, next_actionables, next_is_game_over = game.step(action, action_player_id)

            if next_is_game_over:
                return float("-inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(game)
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(game, min_value, search_depth, next_actionables, next_player_id)
                else:
                    value = self._min_value(game, None, search_depth, next_actionables, next_player_id)

            # αカット
            if alfa is not None and value < alfa:
                return value

            if value <= min_value:
                min_value = value
        
        return min_value

    def _max_value(self, game, beta, search_depth, actionables, action_player_id):
        """
        最大値を返す
        """
        
        max_value = float("-inf")  # マイナス無限

        actionables_list = [1 << i for i in range(actionables.bit_length()) if actionables & (1 << i)]
        
        search_depth += 1  # 探索深さ

        game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }

        for action in actionables_list:
            self.setting_game(game, game_info)
            next_player_id, next_actionables, next_is_game_over = game.step(action, action_player_id)
            
            if next_is_game_over:
                return float("inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(game)
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(game, None, search_depth, next_actionables, next_player_id)
                else:
                    value = self._min_value(game, max_value, search_depth, next_actionables, next_player_id)

            # βカット
            if beta is not None and value > beta:
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
        mask_corner = 0x8100000000000081
        black_corner_count = bin(game.black_board & mask_corner).count("1")
        white_corner_count = bin(game.white_board & mask_corner).count("1")
        
        # 端の数を計算
        mask_edge = 0x7e8181818181817e
        black_edge_count = bin(game.black_board & mask_edge).count("1")
        white_edge_count = bin(game.white_board & mask_edge).count("1")

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
player = MiniMaxV4Player(_id)

# game loop
while True:
    state = ""
    for i in range(board_size):
        line = input()  # rows from top to bottom (viewer perspective).
        state+=line
    
    action_count = int(input())  # number of legal actions for this turn.

    for i in range(action_count):
        action = input()  # the action

    # boardを変換
    black_str = state.replace(".", "0")
    white_str = state.replace("0", "2")
    white_str = white_str.replace("1", "0").replace(".","0").replace("2","1")

    black_board = int(black_str, 2)
    white_board = int(white_str, 2)

    black_count = bin(black_board).count("1")
    white_count = bin(white_board).count("1")

    game_info = {
        "black_board": black_board,
        "white_board": white_board,
        "action_player_id": _id,
        "is_game_over": False,
        "win_player": "",
        "turn": 0,
        "black_count": black_count,
        "white_count": white_count
    }
    print("a: ", file=sys.stderr, flush=True)
    game = Game(game_info)
    print("b: ", file=sys.stderr, flush=True)
    action = player._choice(game)
    print("action: ", action, file=sys.stderr, flush=True)

    # actionを変換(16進数64bitからa8のような形式に変換)
    mask = 0x8000000000000000
    choice_action = ""
    for i in range(64):
        if mask & action != 0:
            choice_action = chr(97 + (i % 8)) + str((i // 8) + 1)
            break
        mask = mask >> 1

    print("choice_action: ", choice_action, file=sys.stderr, flush=True)
    # a-h1-8
    print(choice_action)
import sys
import math
from functools import lru_cache

# -------------------------function-------------------------
@lru_cache()
def get_actionables(player_id, black_board, white_board):
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
    blank_board = ~(black_board | white_board)


    if player_id == "1":
        # 1. 左方向に対してい置ける場所を取得
        white_lr_mask = white_board & mask_lr  # 列1-6かつ白の場所
        white_ud_mask = white_board & mask_ud
        white_mask_lu_ru_ld_rd = white_board & mask_lu_ru_ld_rd

        l_white = (black_board << 1) & white_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
        r_white = (black_board >> 1) & white_lr_mask
        u_white = (black_board << 8) & white_ud_mask
        d_white = (black_board >> 8) & white_ud_mask
        lu_white = (black_board << 9) & white_mask_lu_ru_ld_rd
        ru_white = (black_board << 7) & white_mask_lu_ru_ld_rd
        ld_white = (black_board >> 7) & white_mask_lu_ru_ld_rd
        rd_white = (black_board >> 9) & white_mask_lu_ru_ld_rd

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
        black_lr_mask = black_board & mask_lr  # 列1-6かつ白の場所
        black_ud_mask = black_board & mask_ud
        black_mask_lu_ru_ld_rd = black_board & mask_lu_ru_ld_rd

        l_black = (white_board << 1) & black_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
        r_black = (white_board >> 1) & black_lr_mask
        u_black = (white_board << 8) & black_ud_mask
        d_black = (white_board >> 8) & black_ud_mask
        lu_black = (white_board << 9) & black_mask_lu_ru_ld_rd
        ru_black = (white_board << 7) & black_mask_lu_ru_ld_rd
        ld_black = (white_board >> 7) & black_mask_lu_ru_ld_rd
        rd_black = (white_board >> 9) & black_mask_lu_ru_ld_rd

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

@lru_cache()
def is_actionable(action, player_id, my_player_id, black_board, white_board, is_game_over):
    """
    アクション可能か判定
    """
    # アクション待ちのプレイヤーかどうか
    if my_player_id != player_id:
        return False 
    
    # ゲームが終了しているかどうか
    if is_game_over:
        return False 

    # 可能なアクションの手かどうか
    actionable_list = get_actionables(player_id, black_board, white_board)
    if action not in actionable_list:
        return False 

    return True

@lru_cache()
def check_game_over(black_count, white_count, black_board, white_board):
    """
    ゲームが終了したかどうかを判定
    Returns:
        is_game_over: ゲームが終了したかどうか
        win_player: 勝利したプレイヤー
    """
    result = False
    win_player = ""

    # どちらかの石が0個になった場合
    if black_count == 0:
        return True, "0"
    elif white_count == 0:
        return True, "1"
    
    # 両者ともアクションできない場合
    black_actionables = get_actionables("1", black_board, white_board)
    
    # 光速かのため追加
    if black_actionables != 0:
        return False, ""

    white_actionables = get_actionables("0", black_board, white_board)
    if black_actionables == 0 and white_actionables == 0:
        result = True
        if black_count > white_count:
            win_player = "1"
        elif black_count < white_count:
            win_player = "0"
        else:
            win_player = "2"
    
    return result, win_player

@lru_cache()
def set_board(action, player_id, black_board, white_board):
    """
    ボードの更新
    """
    mask_lr = 0x7e7e7e7e7e7e7e7e
    mask_ud = 0x00ffffffffffff00
    mask_lu_ru_ld_rd = 0x007e7e7e7e7e7e00

    reverse = 0x0000000000000000

    # 石を置く
    if player_id == "1":
        mask_left = mask_lr & white_board  # 左方向
        mask_right = mask_lr & white_board
        mask_up = mask_ud & white_board
        mask_down = mask_ud & white_board
        mask_left_up = mask_lu_ru_ld_rd & white_board
        mask_right_up = mask_lu_ru_ld_rd & white_board
        mask_left_down = mask_lu_ru_ld_rd & white_board
        mask_right_down = mask_lu_ru_ld_rd & white_board

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

        if (l_rev << 1) & black_board != 0:
            reverse |= l_rev
        if (r_rev >> 1) & black_board != 0:
            reverse |= r_rev
        if (u_rev << 8) & black_board != 0:
            reverse |= u_rev
        if (d_rev >> 8) & black_board != 0:
            reverse |= d_rev
        if (lu_rev << 7) & black_board != 0:
            reverse |= lu_rev
        if (ru_rev << 9) & black_board != 0:
            reverse |= ru_rev
        if (ld_rev >> 9) & black_board != 0:
            reverse |= ld_rev
        if (rd_rev >> 7) & black_board != 0:
            reverse |= rd_rev

        black_board |= (action | reverse)
        white_board ^= reverse
    
    elif player_id == "0":
        mask_left = mask_lr & black_board  # 左方向
        mask_right = mask_lr & black_board
        mask_up = mask_ud & black_board
        mask_down = mask_ud & black_board
        mask_left_up = mask_lu_ru_ld_rd & black_board
        mask_right_up = mask_lu_ru_ld_rd & black_board
        mask_left_down = mask_lu_ru_ld_rd & black_board
        mask_right_down = mask_lu_ru_ld_rd & black_board

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
        
        if (l_rev << 1) & white_board != 0:
            reverse |= l_rev
        if (r_rev >> 1) & white_board != 0:
            reverse |= r_rev
        if (u_rev << 8) & white_board != 0:
            reverse |= u_rev
        if (d_rev >> 8) & white_board != 0:
            reverse |= d_rev
        if (lu_rev << 7) & white_board != 0:
            reverse |= lu_rev
        if (ru_rev << 9) & white_board != 0:
            reverse |= ru_rev
        if (ld_rev >> 9) & white_board != 0:
            reverse |= ld_rev
        if (rd_rev >> 7) & white_board != 0:
            reverse |= rd_rev

        white_board |= (action | reverse)
        black_board ^= reverse
    
    return black_board, white_board

@lru_cache()
def step(action, player_id, black_board, white_board, action_player_id):
    """ 
    アクション

    0.01秒早くするためにlru_cacheを使ったため引数にturnが来るはずが消した
    stepした後にturn+=1をする必要あり

    Return:
        next_action_player_id
        actionables: 次アクション可能なリスト
        is_next_game_over: ゲームが終了したかどうか
        game_info: 次のゲーム情報
    """

    # アクションを実行
    next_black_board, next_white_board = set_board(action, player_id, black_board, white_board)

    # 石の数を更新
    
    next_black_count = bin(next_black_board).count("1")
    next_white_count = bin(next_white_board).count("1")

    # ゲームが終了かどうか
    is_next_game_over, win_player = check_game_over(
        next_black_count, next_white_count, next_black_board, next_white_board
    )
    if is_next_game_over:
        end_game_info = {
            "black_board": next_black_board,
            "white_board": next_white_board,
            "black_count": next_black_count,
            "white_count": next_white_count,
            "turn": "",
            "action_player_id": "",
            "win_player": win_player,
            "is_game_over": True
        }
        return "", 0x0, True, end_game_info

    # 次アクション可能なリストを取得
    next_player_id = "0" if action_player_id=="1" else "1"
    actionables = get_actionables(next_player_id, next_black_board, next_white_board)
    
    # 次のアクション可能なプレイヤーを更新
    if actionables == 0:
        actionables = get_actionables(action_player_id, next_black_board, next_white_board)
        next_action_player_id = action_player_id
    else:
        next_action_player_id = next_player_id
    
    next_game_info = {
        "black_board": next_black_board,
        "white_board": next_white_board,
        "black_count": next_black_count,
        "white_count": next_white_count,
        "turn": "",
        "action_player_id": next_action_player_id,
        "win_player": "",
        "is_game_over": False
    }

    return next_action_player_id, actionables, False, next_game_info


class MiniMaxV5Player():
    """
    ゲームインスタンスクラスを使わない
    """
    def __init__(self, player_id=""):
        # "1": 先行(黒)、"0": 後攻(白)
        if player_id != "":
            self.player_id = player_id

    def action(self, game_info):
        """
        アクションをする
        """

        # actionables = game.get_actionables(self.player_id)
        # if actionables == 0:
        #     raise Exception("アクションできません")
        tmp_game_info = game_info.copy()

        action = self._choice(tmp_game_info)

        # ゲーム情報を元に戻す
        next_player_id, actionables, is_next_game_over, next_game_info = step(
            action, self.player_id,
            game_info["black_board"], game_info["white_board"], game_info["action_player_id"]
        )
        next_game_info["turn"] = game_info["turn"]+1

        return next_player_id, actionables, is_next_game_over, next_game_info

    def setting_game(self, game, game_info):
        game.black_board = game_info["black_board"]
        game.white_board = game_info["white_board"]
        game.action_player_id = game_info["action_player_id"]
        game.is_game_over = game_info["is_game_over"]
        game.turn = game_info["turn"]
        game.black_count = game_info["black_count"]
        game.white_count = game_info["white_count"]
    
    def _choice(self, game_info):
        """
        最適な手を選択する
        """
        actionables = get_actionables(self.player_id, game_info["black_board"], game_info["white_board"])
        
        # 価値が最も高い手を選択する
        max_value = float("-inf")  # マイナス無限
        max_action = None

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1

        search_depth = 1  # 探索深さ

        actionables_list.reverse()
        for action in actionables_list:
            tmp_game_info = game_info.copy()
            next_player_id, next_actionables, next_is_game_over, next_game_info = step(
                action, self.player_id,
                tmp_game_info["black_board"], tmp_game_info["white_board"], tmp_game_info["action_player_id"]
            )
            next_game_info["turn"] = tmp_game_info["turn"]+1

            # ゲームが終了した場合
            if next_is_game_over:
                return action
            
            if next_player_id == self.player_id:
                value = self._max_value(None, search_depth, next_actionables, next_player_id, next_game_info)
            else:
                value = self._min_value(max_value, search_depth, next_actionables, next_player_id, next_game_info)

            if value >= max_value:
                max_value = value
                max_action = action
        
        return max_action

    def _min_value(self, alfa, search_depth, actionables, action_player_id, game_info):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1
        
        search_depth += 1

        actionables_list.reverse()
        for action in actionables_list:
            tmp_game_info = game_info.copy()
            next_player_id, next_actionables, next_is_game_over, next_game_info = step(
                action, action_player_id,
                tmp_game_info["black_board"], tmp_game_info["white_board"], tmp_game_info["action_player_id"]
            )
            next_game_info["turn"] = tmp_game_info["turn"]+1

            if next_is_game_over:
                # 引き分けの時は0を返す
                if next_game_info["win_player"] == "2":
                    return 0
                else:
                    return float("-inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                if self.player_id == "1":
                    value = self._evaluate(next_game_info["black_board"], next_game_info["white_board"], next_game_info["black_count"], next_game_info["white_count"])
                elif self.player_id == "0":
                    value = -self._evaluate(next_game_info["black_board"], next_game_info["white_board"], next_game_info["black_count"], next_game_info["white_count"])
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(min_value, search_depth, next_actionables, next_player_id, next_game_info)
                else:
                    value = self._min_value(None, search_depth, next_actionables, next_player_id, next_game_info)

            if value < min_value:
                min_value = value
            
            # αカット
            if alfa is not None and min_value < alfa:
                return min_value
        
        return min_value

    def _max_value(self, beta, search_depth, actionables, action_player_id, game_info):
        """
        最大値を返す
        """
        
        max_value = float("-inf")  # マイナス無限

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1
        
        search_depth += 1  # 探索深さ

        actionables_list.reverse()
        for action in actionables_list:
            tmp_game_info = game_info.copy()
            next_player_id, next_actionables, next_is_game_over, next_game_info = step(
                action, action_player_id,
                tmp_game_info["black_board"], tmp_game_info["white_board"], tmp_game_info["action_player_id"]
            )
            next_game_info["turn"] = tmp_game_info["turn"]+1

            # 引き分けの時は0を返す
            if next_is_game_over:
                if next_game_info["win_player"] == "2":
                    return 0
                else:
                    return float("inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                if self.player_id == "1":
                    value = self._evaluate(next_game_info["black_board"], next_game_info["white_board"], next_game_info["black_count"], next_game_info["white_count"])
                elif self.player_id == "0":
                    value = -self._evaluate(next_game_info["black_board"], next_game_info["white_board"], next_game_info["black_count"], next_game_info["white_count"])
                
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(None, search_depth, next_actionables, next_player_id, next_game_info)
                else:
                    value = self._min_value(max_value, search_depth, next_actionables, next_player_id, next_game_info)

            if value > max_value:
                max_value = value
            
            # βカット
            if beta is not None and max_value > beta:
                return max_value
        
        return max_value
    
    @lru_cache()
    def _evaluate(self, black_board, white_board, black_count, white_count):
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
          + b2,b7,g2,g7のどれかに自分の石がある場合 * -100
          + b2,b7,g2,g7のどれかに相手の石がある場合 * -100
        """
        black_corner_count = 0
        white_corner_count = 0
        black_near_corner_count = 0
        white_near_corner_count = 0
        black_edge_count = 0
        white_edge_count = 0
        result = 0

        # 角の数を計算
        mask_corner = 0x8100000000000081
        black_corner_count = bin(black_board & mask_corner).count("1")
        white_corner_count = bin(white_board & mask_corner).count("1")

        # 角ちか
        mask_near_corner_ur = 0x0203000000000000
        mask_near_corner_ul = 0x40c0000000000000
        mask_near_corner_dr = 0x0000000000000302
        mask_near_corner_dl = 0x000000000000c040

        mask_corner_ur = 0x0100000000000000
        mask_corner_ul = 0x8000000000000000
        mask_corner_dr = 0x0000000000000001
        mask_corner_dl = 0x0000000000000080

        blank_board = ~(black_board | white_board)
        # 角が空白の時
        if mask_corner_ur & blank_board != 0:
            black_near_corner_count += bin(mask_near_corner_ur & black_board).count("1")
            white_near_corner_count += bin(mask_near_corner_ur & white_board).count("1")
        if mask_corner_ul & blank_board != 0:
            black_near_corner_count += bin(mask_near_corner_ul & black_board).count("1")
            white_near_corner_count += bin(mask_near_corner_ul & white_board).count("1")
        if mask_corner_dr & blank_board != 0:
            black_near_corner_count += bin(mask_near_corner_dr & black_board).count("1")
            white_near_corner_count += bin(mask_near_corner_dr & white_board).count("1")
        if mask_corner_dl & blank_board != 0:
            black_near_corner_count += bin(mask_near_corner_dl & black_board).count("1")
            white_near_corner_count += bin(mask_near_corner_dl & white_board).count("1")

        # 端の数を計算
        mask_edge = 0x7e8181818181817e
        black_edge_count = bin(black_board & mask_edge).count("1")
        white_edge_count = bin(white_board & mask_edge).count("1")

        # 評価値を計算
        result += black_count * 1
        result += white_count * -1
        result += black_corner_count * 100
        result += white_corner_count * -100
        result += black_near_corner_count * -100
        result += white_near_corner_count * 100
        result += black_edge_count * 10
        result += white_edge_count * -10

        return result 
    
# -------------------------/function-------------------------

_id = input()  # id of your player.
board_size = int(input())
player = MiniMaxV5Player(_id)

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
    action = player._choice(game_info)
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
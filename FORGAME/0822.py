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


    if player_id == 1:
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

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

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
    elif player_id == 0:
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

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

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
def set_board(action, player_id, black_board, white_board):
    """
    ボードの更新
    """
    mask_lr = 0x7e7e7e7e7e7e7e7e
    mask_ud = 0x00ffffffffffff00
    mask_lu_ru_ld_rd = 0x007e7e7e7e7e7e00

    reverse = 0x0000000000000000

    # 石を置く
    if player_id == 1:
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
    
    elif player_id == 0:
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

class MiniMaxV6V3Player():
    """
    ゲームクラス3を使用
    negamax(depth4)
    """
    EVALUATE_MASK_NOT25 = 0x42c300000000c342
    EVALUATE_MASK_1 = 0x0000182424180000
    EVALUATE_MASK_2 = 0x003c425a5a423c00
    EVALUATE_MASK_5 = 0x1800248181240018
    EVALUATE_MASK_10 = 0x2400810000810024
    EVALUATE_MASK_100 = 0x8100000000000081

    def __init__(self, player_id=""):
        # "1": 先行(黒)、"0": 後攻(白)
        if player_id != "":
            self.player_id = player_id

    def action(self, black_board, white_board, actionables):
        """
        アクションをする
        """

        # actionables = game.get_actionables(self.player_id)
        # if actionables == 0:
        #     raise Exception("アクションできません")

        action = self._choice(black_board, white_board, actionables)

        # ゲーム情報を元に戻す
        black_board, white_board = set_board(action, self.player_id, black_board, white_board)

        return black_board, white_board
    
    @lru_cache()
    def get_actionables_list(self, actionables):
        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1
        return actionables_list
    
    def _choice(self, black_board, white_board, actionables):
        """
        最適な手を選択する
        """
        # 価値が最も高い手を選択する
        alpha = float("-inf")  # マイナス無限
        beta = float("inf")

        max_action = None

        actionables_list = self.get_actionables_list(actionables)

        search_depth = 0  # 探索深さ

        actionables_list.reverse()
        for action in actionables_list:
            next_black_board, next_white_board = set_board(action, self.player_id, black_board, white_board)

            next_action_player_id = 1 - self.player_id
            
            value = - self.nega_ab(next_action_player_id, next_black_board, next_white_board, search_depth+1, False, -beta, -alpha)

            if value > alpha:
                alpha = value
                max_action = action
        
        return max_action

    def nega_ab(self, action_player_id, black_board, white_board, depth, is_pass, alpha, beta):
        """
        nega_alpha_beta法
        """
        if depth == 4:
            return self._evaluate(action_player_id, black_board, white_board)

        max_value = float("-inf")  # マイナス無限
        
        actionables = get_actionables(action_player_id, black_board, white_board)
        actionables_list = self.get_actionables_list(actionables)
        for action in actionables_list:
            next_black_board, next_white_board = set_board(action, action_player_id, black_board, white_board)

            next_action_player_id = 1 - action_player_id

            value = -self.nega_ab(next_action_player_id, next_black_board, next_white_board, depth+1, False, -beta, -alpha)

            # betaカット
            if value >= beta:
                return value
            
            alpha = max(alpha, value)
            max_value = max(max_value, value)
        
        # パスの場合(max_valueが-infのまま)
        if max_value == float("-inf"):
            # 2回連続でパスの場合
            if (is_pass):
                return self._evaluate(action_player_id, black_board, white_board)
            
            next_action_player_id = 1 - action_player_id
            return - self.nega_ab(next_action_player_id, black_board, white_board, depth, True, -beta, -alpha)
        
        return max_value
    
    @lru_cache()
    def _evaluate(self, action_player_id, black_board, white_board):
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
        black_count = bin(black_board).count("1")
        white_count = bin(white_board).count("1")
        black_corner_count = 0
        white_corner_count = 0
        black_edge_count = 0
        white_edge_count = 0
        result = 0

        # 角の数を計算
        mask_corner = 0x8100000000000081
        black_corner_count = bin(black_board & mask_corner).count("1")
        white_corner_count = bin(white_board & mask_corner).count("1")
        
        # 端の数を計算
        mask_edge = 0x7e8181818181817e
        black_edge_count = bin(black_board & mask_edge).count("1")
        white_edge_count = bin(white_board & mask_edge).count("1")

        # 評価値を計算
        if action_player_id == 1:
            result += black_count * 1
            result += white_count * -1
            result += black_corner_count * 100
            result += white_corner_count * -100
            result += black_edge_count * 10
            result += white_edge_count * -10
        elif action_player_id == 0:
            result += black_count * -1
            result += white_count * 1
            result += black_corner_count * -100
            result += white_corner_count * 100
            result += black_edge_count * -10
            result += white_edge_count * 10
        
        return result 
    
# -------------------------/function-------------------------

_id = int(input())  # id of your player.
board_size = int(input())
player = MiniMaxV6V3Player(_id)

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

    actionables = get_actionables(_id, black_board, white_board)

    action = player._choice(black_board, white_board, actionables)
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
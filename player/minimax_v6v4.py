from player.abstruct import Player
import random
import copy
import logging
import time
from game3 import *
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class MiniMaxV6V4Player(Player):
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
        
        # 探索数ノード調査
        self.count = 0  # 1アクションごとの探索数
        self.count_list = []
        self.time_list = []
        self.total_count = 0  # 1戦ごとの探索数

    def action(self, black_board, white_board, actionables):
        """
        アクションをする
        """
        start_time = time.time()

        # actionables = game.get_actionables(self.player_id)
        # if actionables == 0:
        #     raise Exception("アクションできません")

        action = self._choice(black_board, white_board, actionables)

        # ゲーム情報を元に戻す
        black_board, white_board = set_board(action, self.player_id, black_board, white_board)

        # debug
        self.count_list.append(self.count)
        self.time_list.append(time.time() - start_time)
        self.total_count += self.count
        self.count = 0

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

            self.count += 1
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

            self.count += 1
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
        blank_count = bin(blank_board & 0xffffffffffffffff).count("1")
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

        if action_player_id == 1:
            result += black_count * 1
            result += white_count * -1
            result += black_corner_count * 400
            result += white_corner_count * -400
            result += black_near_corner_count * -100
            result += white_near_corner_count * 100
            result += black_edge_count * 10
            result += white_edge_count * -10
        elif action_player_id == 0:
            result += black_count * -1
            result += white_count * 1
            result += black_corner_count * -400
            result += white_corner_count * 400
            result += white_near_corner_count * -100
            result += black_near_corner_count * 100
            result += black_edge_count * -10
            result += white_edge_count * 10
        else:
            logger.error("不正なプレイヤーIDです")

        return result 
    
    
    



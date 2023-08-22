from player.abstruct import Player
import random
import copy
import logging
import time
from game3 import *
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class MiniMaxV6V3Player(Player):
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
        if action_player_id == 1:
            my_board = black_board
            opponent_board = white_board
        else:
            my_board = white_board
            opponent_board = black_board

        result = 0
        result += bin(self.EVALUATE_MASK_NOT25 & my_board).count("1") * -25
        result += bin(self.EVALUATE_MASK_NOT25 & opponent_board).count("1") * 25

        result += bin(self.EVALUATE_MASK_1 & my_board).count("1") * 1
        result += bin(self.EVALUATE_MASK_1 & opponent_board).count("1") * -1

        result += bin(self.EVALUATE_MASK_2 & my_board).count("1") * 2
        result += bin(self.EVALUATE_MASK_2 & opponent_board).count("1") * -2

        result += bin(self.EVALUATE_MASK_5 & my_board).count("1") * 5
        result += bin(self.EVALUATE_MASK_5 & opponent_board).count("1") * -5

        result += bin(self.EVALUATE_MASK_10 & my_board).count("1") * 10
        result += bin(self.EVALUATE_MASK_10 & opponent_board).count("1") * -10

        result += bin(self.EVALUATE_MASK_100 & my_board).count("1") * 100
        result += bin(self.EVALUATE_MASK_100 & opponent_board).count("1") * -100

        return result
    
    



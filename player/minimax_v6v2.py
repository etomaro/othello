from player.abstruct import Player
import random
import copy
import logging
import time
from game3 import *
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class MiniMaxV6V2Player(Player):
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
    
    # def _choice(self, black_board, white_board, actionables):

    #     get_actionables_list = self.get_actionables_list(actionables)

    #     action = random.choice(get_actionables_list)

    #     return action
    
    def _choice(self, black_board, white_board, actionables):
        """
        最適な手を選択する
        """
        # 価値が最も高い手を選択する
        max_value = float("-inf")  # マイナス無限
        max_action = None

        actionables_list = self.get_actionables_list(actionables)

        search_depth = 1  # 探索深さ

        actionables_list.reverse()
        for action in actionables_list:
            next_black_board, next_white_board = set_board(action, self.player_id, black_board, white_board)

            self.count += 1

            next_action_player_id = 1 - self.player_id

            next_actionables = get_actionables(next_action_player_id, next_black_board, next_white_board)
            # skipまたはゲーム終了判定
            if bin(next_actionables).count("1") == 0:
                next_action_player_id = 1 - next_action_player_id
                next_actionables = get_actionables(next_action_player_id, next_black_board, next_white_board)

                if bin(next_actionables).count("1") == 0:
                    # ゲーム終了
                    return action
            
            if next_action_player_id == self.player_id:
                value = self._max_value(None, search_depth, next_actionables, black_board, white_board)
            else:
                value = self._min_value(max_value, search_depth, next_actionables, black_board, white_board)

            if value >= max_value:
                max_value = value
                max_action = action
            
            # if self.count > 500:
            #     return max_action
        
        return max_action

    def _min_value(self, alfa, search_depth, actionables, black_board, white_board):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限

        actionables_list = self.get_actionables_list(actionables)
        
        search_depth += 1

        action_player_id = 1 - self.player_id

        actionables_list.reverse()
        for action in actionables_list:
            next_black_board, next_white_board = set_board(action, action_player_id, black_board, white_board)
            
            self.count += 1
            
            next_action_player_id = 1 - action_player_id
            next_actionables = get_actionables(next_action_player_id, next_black_board, next_white_board)

            if bin(next_actionables).count("1") == 0:
                next_action_player_id = 1 - next_action_player_id
                next_actionables = get_actionables(next_action_player_id, next_black_board, next_white_board)
                if bin(next_actionables).count("1") == 0:
                    # ゲーム終了
                    # 引き分けか相手の勝ちか判定
                    black_count = bin(next_black_board).count("1")
                    white_count = bin(next_white_board).count("1")
                    if self.player_id == 0:
                        if black_count > white_count:
                            return float("-inf")
                        else:
                            return 0
                    else:
                        if black_count < white_count:
                            return float("-inf")
                        else:
                            return 0
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(next_black_board, next_white_board)
            else:
                if next_action_player_id == self.player_id:
                    value = self._max_value(min_value, search_depth, next_actionables, next_black_board, next_white_board)
                else:
                    value = self._min_value(None, search_depth, next_actionables, next_black_board, next_white_board)

            if value < min_value:
                min_value = value
            
            # αカット
            if alfa is not None and min_value < alfa:
                return min_value
        
        return min_value

    def _max_value(self, beta, search_depth, actionables, black_board, white_board):
        """
        最大値を返す
        """
        
        max_value = float("-inf")  # マイナス無限

        actionables_list = self.get_actionables_list(actionables)
        
        search_depth += 1  # 探索深さ

        action_player_id = self.player_id

        actionables_list.reverse()
        for action in actionables_list:
            next_black_board, next_white_board = set_board(action, action_player_id, black_board, white_board)

            self.count += 1

            next_action_player_id = 1 - action_player_id
            next_actionables = get_actionables(next_action_player_id, next_black_board, next_white_board)

            if bin(next_actionables).count("1") == 0:
                next_action_player_id = 1 - next_action_player_id
                next_actionables = get_actionables(next_action_player_id, next_black_board, next_white_board)
                if bin(next_actionables).count("1") == 0:
                    # ゲーム終了
                    # 引き分けか相手の勝ちか判定
                    black_count = bin(next_black_board).count("1")
                    white_count = bin(next_white_board).count("1")
                    if self.player_id == 0:
                        if black_count < white_count:
                            return float("inf")
                        else:
                            return 0
                    else:
                        if black_count > white_count:
                            return float("inf")
                        else:
                            return 0
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(next_black_board, next_white_board)
                
            else:
                if next_action_player_id == self.player_id:
                    value = self._max_value(None, search_depth, next_actionables, next_black_board, next_white_board)
                else:
                    value = self._min_value(max_value, search_depth, next_actionables, next_black_board, next_white_board)

            if value > max_value:
                max_value = value
            
            # βカット
            if beta is not None and max_value > beta:
                return max_value
        
        return max_value
    
    @lru_cache()
    def _evaluate(self, black_board, white_board):
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
        if self.player_id == 1:
            my_board = black_board
        else:
            my_board = white_board

        result = 0
        result += bin(self.EVALUATE_MASK_NOT25 & my_board).count("1") * -25

        result += bin(self.EVALUATE_MASK_1 & my_board).count("1") * 1

        result += bin(self.EVALUATE_MASK_2 & my_board).count("1") * 2

        result += bin(self.EVALUATE_MASK_5 & my_board).count("1") * 5

        result += bin(self.EVALUATE_MASK_10 & my_board).count("1") * 10

        result += bin(self.EVALUATE_MASK_100 & my_board).count("1") * 100

        return result
    
    



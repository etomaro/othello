from player.abstruct import Player
import random
import copy
import logging
import time
from game2 import *
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class MiniMaxV5Player(Player):
    """
    ゲームインスタンスクラスを使わない
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

    def action(self, game_info):
        """
        アクションをする
        """
        start_time = time.time()

        # actionables = game.get_actionables(self.player_id)
        # if actionables == 0:
        #     raise Exception("アクションできません")
        tmp_game_info = game_info.copy()

        action = self._choice(tmp_game_info)

        # ゲーム情報を元に戻す
        next_player_id, actionables, is_next_game_over, next_game_info = step(
            action,
            game_info["black_board"], game_info["white_board"], game_info["action_player_id"]
        )
        next_game_info["turn"] = game_info["turn"]+1

        # debug
        self.count_list.append(self.count)
        self.time_list.append(time.time() - start_time)
        self.total_count += self.count
        self.count = 0

        return next_player_id, actionables, is_next_game_over, next_game_info
    
    @lru_cache()
    def get_actionables_list(self, actionables):
        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1
        return actionables_list
    
    def _choice(self, game_info):
        """
        最適な手を選択する
        """
        actionables = get_actionables(self.player_id, game_info["black_board"], game_info["white_board"])
        if actionables == 0:
            raise Exception("アクションできません")
        
        # 価値が最も高い手を選択する
        max_value = float("-inf")  # マイナス無限
        max_action = None

        actionables_list = self.get_actionables_list(actionables)

        search_depth = 1  # 探索深さ

        actionables_list.reverse()
        for action in actionables_list:
            tmp_game_info = game_info.copy()
            next_player_id, next_actionables, next_is_game_over, next_game_info = step(
                action,
                tmp_game_info["black_board"], tmp_game_info["white_board"], tmp_game_info["action_player_id"]
            )
            next_game_info["turn"] = tmp_game_info["turn"]+1

            self.count += 1

            # ゲームが終了した場合
            if next_is_game_over:
                return action
            
            if next_player_id == self.player_id:
                value = self._max_value(None, search_depth, next_actionables, next_game_info)
            else:
                value = self._min_value(max_value, search_depth, next_actionables, next_game_info)

            if value >= max_value:
                max_value = value
                max_action = action
            
            # if self.count > 500:
            #     return max_action
        
        return max_action

    def _min_value(self, alfa, search_depth, actionables, game_info):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限

        actionables_list = self.get_actionables_list(actionables)
        
        search_depth += 1

        actionables_list.reverse()
        for action in actionables_list:
            tmp_game_info = game_info.copy()
            next_player_id, next_actionables, next_is_game_over, next_game_info = step(
                action,
                tmp_game_info["black_board"], tmp_game_info["white_board"], tmp_game_info["action_player_id"]
            )
            next_game_info["turn"] = tmp_game_info["turn"]+1
            
            self.count += 1

            if next_is_game_over:
                # 引き分けの時は0を返す
                if next_game_info["win_player"] == "2":
                    return 0
                else:
                    return float("-inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(next_game_info["black_board"])
                if self.player_id == "0":
                    value = -value
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(min_value, search_depth, next_actionables, next_game_info)
                else:
                    value = self._min_value(None, search_depth, next_actionables, next_game_info)

            if value < min_value:
                min_value = value
            
            # αカット
            if alfa is not None and min_value < alfa:
                return min_value
        
        return min_value

    def _max_value(self, beta, search_depth, actionables, game_info):
        """
        最大値を返す
        """
        
        max_value = float("-inf")  # マイナス無限

        actionables_list = self.get_actionables_list(actionables)
        
        search_depth += 1  # 探索深さ

        actionables_list.reverse()
        for action in actionables_list:
            tmp_game_info = game_info.copy()
            next_player_id, next_actionables, next_is_game_over, next_game_info = step(
                action,
                tmp_game_info["black_board"], tmp_game_info["white_board"], tmp_game_info["action_player_id"]
            )
            next_game_info["turn"] = tmp_game_info["turn"]+1

            self.count += 1

            # 引き分けの時は0を返す
            if next_is_game_over:
                if next_game_info["win_player"] == "2":
                    return 0
                else:
                    return float("inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(next_game_info["black_board"])
                if self.player_id == "0":
                    value = -value
                
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(None, search_depth, next_actionables, next_game_info)
                else:
                    value = self._min_value(max_value, search_depth, next_actionables, next_game_info)

            if value > max_value:
                max_value = value
            
            # βカット
            if beta is not None and max_value > beta:
                return max_value
        
        return max_value
    
    @lru_cache()
    def _evaluate(self, my_board):
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
        result = 0
        result += bin(self.EVALUATE_MASK_NOT25 & my_board).count("1") * -25

        result += bin(self.EVALUATE_MASK_1 & my_board).count("1") * 1

        result += bin(self.EVALUATE_MASK_2 & my_board).count("1") * 2

        result += bin(self.EVALUATE_MASK_5 & my_board).count("1") * 5

        result += bin(self.EVALUATE_MASK_10 & my_board).count("1") * 10

        result += bin(self.EVALUATE_MASK_100 & my_board).count("1") * 100

        return result
    
    



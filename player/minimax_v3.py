from player.abstruct import Player
import random
import copy
import logging
import time


logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class MiniMaxV3Player(Player):
    """
    4手先まで行動(自分と相手が一回ずつ行動)した後の状態で価値を決めて、min(),max()で最適な手を選択する
    評価関数を設定
    """
    def __init__(self, player_id=""):
        # "1": 先行(黒)、"0": 後攻(白)
        if player_id != "":
            self.player_id = player_id
        
        # 探索数ノード調査
        self.count = 0  # 1アクションごとの探索数
        self.count_list = []
        self.time_list = []
        self.total_count = 0  # 1戦ごとの探索数

    def action(self, game):
        """
        アクションをする
        """
        start_time = time.time()

        # actionables = game.get_actionables(self.player_id)
        # if len(actionables) == 0:
        #     raise Exception("アクションできません")
        
        tmp_game = copy.deepcopy(game)
        action = self._choice(tmp_game)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        # debug
        self.count_list.append(self.count)
        self.time_list.append(time.time() - start_time)
        self.total_count += self.count
        self.count = 0

        return next_player_id, actionables, is_game_over
    
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

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1
        
        for action in actionables_list:
            next_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = next_game.step(action, self.player_id)

            self.count += 1

            # ゲームが終了した場合
            if next_is_game_over:
                return action
            
            value = self._min_value(next_game)
            if value >= max_value:
                max_value = value
                max_action = action
        
        return max_action

    def _min_value(self, game):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限
        opponent_player_id = "1" if self.player_id == "0" else "0"
        actionables = game.get_actionables(opponent_player_id)

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1

        for action in actionables_list:
            new_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = new_game.step(action, opponent_player_id)
            
            self.count += 1

            if next_is_game_over:
                return float("-inf")
            
            # 状態の価値を計算
            value = self._max2_value(new_game)
            if value <= min_value:
                min_value = value
        
        return min_value

    def _min2_value(self, game):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限
        opponent_player_id = "1" if self.player_id == "0" else "0"
        actionables = game.get_actionables(opponent_player_id)

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1

        for action in actionables_list:
            new_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = new_game.step(action, opponent_player_id)
            
            self.count += 1

            if next_is_game_over:
                return float("-inf")
            
            # 状態の価値を計算
            value = self._evaluate(new_game)
            if value <= min_value:
                min_value = value

        return min_value

    def _max2_value(self, game):
        """
        最大値を返す
        """
        
        max_value = float("-inf")  # マイナス無限
        actionables = game.get_actionables(self.player_id)

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1

        for action in actionables_list:
            new_game = copy.deepcopy(game)  # インスタンスの値コピー
            next_player_id, next_actionables, next_is_game_over = new_game.step(action, self.player_id)
            
            self.count += 1

            if next_is_game_over:
                return float("inf")
            
            # 状態の価値を計算
            value = self._min2_value(new_game)
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
        else:
            logger.error("不正なプレイヤーIDです")
        
        return result 
    



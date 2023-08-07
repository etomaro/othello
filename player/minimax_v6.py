from player.abstruct import Player
import random
import copy
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class MiniMaxV6Player(Player):
    """
    MINIMAXを導入
      mini_value()の時にαカットを検討
      max2_value()の時にβカットを検討
      mini2_value()の時にαカットを検討
      max3_value()の時にβカットを検討
      mini3_value()の時にαカットを検討
    6手先まで行動(自分と相手が一回ずつ行動)した後の状態で価値を決めて、min(),max()で最適な手を選択する
    評価関数をUpdate
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
        action = self._choice(tmp_game)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        # debug
        result = ""
        for i in range(8):
            for j in range(8):
                result += game.board[i][j]
                result += " "
            result += "\n"
        
        logger.info(f"---{game.turn}回目---\n{result}\n")
        logger.info("minimax_v3 action: %s\n", action)

        return next_player_id, actionables, is_game_over
    
    def _choice(self, game):
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
            value = self._max3_value(new_game, min_value)

            # αカット
            if value < alfa:
                return value

            if value <= min_value:
                min_value = value

        return min_value
    
    def _max3_value(self, game, beta):
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
            value = self._min3_value(new_game, max_value)

            # βカット
            if value > beta:
                return value

            if value >= max_value:
                max_value = value
        
        return max_value

    def _min3_value(self, game, alfa):
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

    def _evaluate(self, game):
        """
        葉ノードの評価値を計算(末端ノード)

        ゲームが終了した場合+10000 or -10000を返す
        評価方法
          + 自分の角の数 * 10000
          + 相手の角の数 * -10000
          + 自分の端の数 * 100
          + 相手の端の数 * -100
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
            result += black_corner_count * 10000
            result += white_corner_count * -10000
            result += black_edge_count * 100
            result += white_edge_count * -100
        elif self.player_id == "0":
            result += black_count * -1
            result += white_count * 1
            result += black_corner_count * -10000
            result += white_corner_count * 10000
            result += black_edge_count * -100
            result += white_edge_count * 100
        else:
            logger.error("不正なプレイヤーIDです")
        
        return result 
    



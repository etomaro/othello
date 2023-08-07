from player.abstruct import Player
import random
import copy


class MiniMaxV1Player(Player):
    """
    2手先まで行動(自分と相手が一回ずつ行動)した後の状態で価値を決めて、min(),max()で最適な手を選択する
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
            
            value = self._min_value(next_game)
            if value >= max_value:
                max_value = value
                max_action = action
        
        return max_action

    def _min_value(self, game):
        """
        最小値を返す
        """
        if game.is_game_over:
            return self._evaluate(game)
        
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
            if value <= min_value:
                min_value = value
        
        return min_value

    def _evaluate(self, game):
        """
        葉ノードの評価値を計算(末端ノード)

        ゲームが終了した場合+10000 or -10000を返す
        一旦石の数で評価する
        """
        black_count = game.black_count
        white_count = game.white_count

        result = ""
        if self.player_id == "1":
            result = black_count - white_count
        else:
            result = white_count - black_count
        
        return result 
    



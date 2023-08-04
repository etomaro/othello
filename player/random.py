from player.abstruct import Player
import random


class RandomPlayer(Player):
    def __init__(self, player_id):
        self.player_id = player_id  # "1": 先行(黒)、"0": 後攻(白)

    def action(self, game):
        """
        アクションをする
        """
        actionables = game.get_actionables(self.player_id)
        if len(actionables) == 0:
            raise Exception("アクションできません")
        
        action = random.choice(actionables)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        return next_player_id, actionables, is_game_over
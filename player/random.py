from player.abstruct import Player
import random


class RandomPlayer(Player):
    def __init__(self, player_id=""):
        # "1": 先行(黒)、"0": 後攻(白)
        if player_id != "":
            self.player_id = player_id

    def action(self, game):
        """
        アクションをする
        """
        actionables = game.get_actionables(self.player_id)
        if actionables == 0:
            raise Exception("アクションできません")
        
        # ランダムに手を選択する
        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1

        action = random.choice(actionables_list)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        return next_player_id, actionables, is_game_over
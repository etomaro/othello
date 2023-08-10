from player.abstruct import Player
import random


class HumanPlayer(Player):
    def __init__(self, player_id=""):
        # "1": 先行(黒)、"0": 後攻(白)
        if player_id != "":
            self.player_id = player_id

    def action(self, game):
        """
        アクションをする
        """
        # 状態を出力
        game.print_board()

        actionables = game.get_actionables(self.player_id)
        # actionables_debug = bin(actionables)[2:].zfill(64)
        # print("アクション可能な場所")
        # for i in range(8):
        #     print(actionables_debug[i*8:i*8+8])
        if actionables == 0:
            raise Exception("アクションできません")
        
        while True:
            action_row = input("アクションする行を入力してください(0-7)")
            try:
                action_row = int(action_row)
                if action_row < 0 or action_row > 7:
                    ValueError
            except ValueError:
                print("行は0-7の間で入力してください")
                continue
            action_col = input("アクションする列を入力してください(0-7)")
            try:
                action_col = int(action_col)
                if action_col < 0 or action_col > 7:
                    ValueError
            except ValueError:
                print("列は0-7の間で入力してください")
                continue
            
            mask = 0x8000000000000000
            action = mask >> (action_row * 8 + action_col)
            if (action & actionables) != 0:
                break
            else:
                print(f"アクションが不正です。{actionables}の中から選んでください")
                print(action)
                continue
        
        print(f"アクション: {bin(action)[2:].zfill(64)}")
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        return next_player_id, actionables, is_game_over
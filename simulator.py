from game import Game
from player.random import RandomPlayer
from player.human import HumanPlayer


class Simulator():
    def __init__(self, player1, player0):
        """
        引数にPlayerインスタンスを受け取る
        """
        self.player1 = player1
        self.player0 = player0

        player1.player_id = "1"  # 先行
        player0.player_id = "0"  # 後攻

        self.game = Game()  # ゲームインスタンス作成

    def run(self):
        """
        ゲームを実行する
        """
        action_player = self.player1  # 先行のプレイヤーからスタート
        while True:
            next_player_id, actionables, is_game_over = action_player.action(self.game)
            if is_game_over:
                break

            # 次のプレイヤーを決定
            if next_player_id == "1":
                action_player = self.player1
            elif next_player_id == "0":
                action_player = self.player0
            else:
                raise Exception("不正なプレイヤーIDです")
            

        game_result = self.game.get_result()
        print("---ゲーム終了---")
        print(f"勝者: {game_result['win_player']}")
        print("先行の石の数: ", game_result["black_count"])
        print("後攻の石の数: ", game_result["white_count"])


# ---test---
player1 = RandomPlayer("1")
player0 = HumanPlayer("0")
simulator = Simulator(player1, player0)
simulator.run()




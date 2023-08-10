from game import Game
import time
import logging
from player.random import RandomPlayer
from player.human import HumanPlayer
from player.firstModel import FirstModelPlayer
from player.minimax_v1 import MiniMaxV1Player
from player.minimax_v2 import MiniMaxV2Player
from player.minimax_v3 import MiniMaxV3Player
from player.minimax_v4 import MiniMaxV4Player
from player.minimax_v5 import MiniMaxV5Player
from player.minimax_v6 import MiniMaxV6Player
from player.minimax_v4v2 import MiniMaxV4V2Player

logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)

class Simulator():
    def __init__(self, player1, player0):
        """
        引数にPlayerインスタンスを受け取る
        """
        self.player1 = player1
        self.player0 = player0

        self.player1.player_id = "1"  # 先行
        self.player0.player_id = "0"  # 後攻

        self.game = Game()  # ゲームインスタンス作成

    def run(self):
        """
        ゲームを実行する
        """
        action_player = self.player1  # 先行のプレイヤーからスタート
        while True:
            ##debug
            # result = ""
            # for i in range(8):
            #     for j in range(8):
            #         result += self.game.board[i][j]
            #         result += " "
            #     result += "\n"
            
            # logger.info(f"---{self.game.turn}回目---\n{result}\n")

            next_player_id, actionables, is_game_over = action_player.action(self.game)
            if is_game_over:
                return self.game.get_result()

            # 次のプレイヤーを決定
            if next_player_id == "1":
                action_player = self.player1
            elif next_player_id == "0":
                action_player = self.player0
            else:
                raise Exception("不正なプレイヤーIDです")
            

        game_result = self.game.get_result()
        logger.debug("---ゲーム終了---")
        logger.debug(f"勝者: {game_result['win_player']}")
        logger.debug("先行の石の数: ", game_result["black_count"])
        logger.debug("後攻の石の数: ", game_result["white_count"])

# ---1回test---
first_player = MiniMaxV4Player()
second_player = MiniMaxV4V2Player()
simulator = Simulator(first_player, second_player)
start = time.time()
game_result = simulator.run()
logger.info("v4 vs v2")
logger.info(f"勝者: {game_result['win_player']}")
logger.info(f"先行の石の数: {game_result['black_count']}")
logger.info(f"後攻の石の数: {game_result['white_count']}")
logger.info(f"ターン数: {game_result['turn']}")
logger.info(f"処理時間: {time.time() - start}")
logger.info("1アクションの探索数: %s", first_player.count_list)
logger.info("1アクションの探索平均数: %s", sum(first_player.count_list) / len(first_player.count_list))
logger.info("1アクションの探索の最大値: %s", max(first_player.count_list))
logger.info("1アクションの時間: %s", first_player.time_list)
logger.info("1アクションの時間平均: %s", sum(first_player.time_list) / len(first_player.time_list))
logger.info("1アクションの時間の最大値: %s", max(first_player.time_list))
logger.info("1戦の探索数: %s", first_player.total_count)

# ---100回test---
# first_win_count = 0
# second_win_count = 0
# draw_count = 0

# first_player = MiniMaxV4Player()
# second_player = RandomPlayer()

# 時間を測定
# start = time.time()
# for i in range(10):
#     simulator = Simulator(first_player, second_player)
#     result = simulator.run()
#     if result["win_player"] == "1":
#         first_win_count += 1
#     elif result["win_player"] == "0":
#         second_win_count += 1
#     elif result["win_player"] == "2":
#         draw_count += 1
#     else:
#         raise Exception("不正な勝者です")

#     logger.info(f"---{i}回目のゲーム終了---")


# print("minimax_v4 vs random")
# logger.info(f"先行の勝利数: {first_win_count}")
# logger.info(f"後攻の勝利数: {second_win_count}")
# logger.info(f"引き分け数: {draw_count}")
# logger.info(f"処理時間: {time.time() - start}")




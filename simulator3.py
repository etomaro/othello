from game3 import *
import time
import logging
from player.minimax_v6 import MiniMaxV6Player
from player.minimax_v6v2 import MiniMaxV6V2Player
from player.minimax_v6v3 import MiniMaxV6V3Player
from player.minimax_v6v4 import MiniMaxV6V4Player
from player.minimax_v6v5 import MiniMaxV6V5Player


logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)

class Simulator():
    def __init__(self, player1, player0):
        """
        引数にPlayerインスタンスを受け取る
        """
        self.player1 = player1
        self.player0 = player0

        self.player1.player_id = 1  # 先行
        self.player0.player_id = 0  # 後攻

    def run(self):
        """
        ゲームを実行する
        """
        action_player = self.player1  # 先行のプレイヤーからスタート
        action_player_id = 1
        black_board, white_board, actionables = get_game_init()
        while True:
            ##debug
            # result = ""
            # for i in range(8):
            #     for j in range(8):
            #         result += self.game.board[i][j]
            #         result += " "
            #     result += "\n"
            
            # logger.info(f"---{self.game.turn}回目---\n{result}\n")

            black_board, white_board = action_player.action(black_board, white_board, actionables)
            # print("ブランクボード")
            # blank_board = ~(black_board | white_board)
            # print(blank_board)
            # print(bin(blank_board & 0xffffffffffffffff).count("1"))
            # # print(bin(blank_board & 0xffffffffffffffff))  
            # print()            
            
            # debug
            # print_board(black_board, white_board)

            action_player_id = 1 -action_player_id

            actionables = get_actionables(action_player_id, black_board, white_board)
            if bin(actionables).count("1") == 0:
                action_player_id = 1 - action_player_id
                actionables = get_actionables(action_player_id, black_board, white_board)

                if bin(actionables).count("1") == 0:
                    # ゲーム終了
                    return get_game_info(black_board, white_board)

            # プレイヤー交代
            if action_player_id == 1:
                action_player = self.player1
            else:
                action_player = self.player0

# ---1回test---
if __name__ == "__main__":
    first_player = MiniMaxV6V5Player()
    second_player = MiniMaxV6V3Player()
    simulator = Simulator(first_player, second_player)
    start = time.time()
    black_count, white_count, win_player = simulator.run()
    logger.info("v6 vs v6")
    logger.info(f"勝者: {win_player}")
    logger.info(f"先行の石の数: {black_count}")
    logger.info(f"後攻の石の数: {white_count}")
    logger.info(f"処理時間: {time.time() - start}")
    logger.info("1アクションの探索数: %s", first_player.count_list)
    logger.info("1アクションの探索平均数: %s", sum(first_player.count_list) / len(first_player.count_list))
    logger.info("1アクションの探索の最大値: %s", max(first_player.count_list))
    logger.info("1アクションの時間: %s", first_player.time_list)
    logger.info("1アクションの時間平均: %s", sum(first_player.time_list) / len(first_player.time_list))
    logger.info("1アクションの時間の最大値: %s", max(first_player.time_list))
    logger.info("1戦の探索数: %s", first_player.total_count)
from player.abstruct import Player
import random
import copy
import logging
import time


logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class MiniMaxV4V2Player(Player):
    """
    MINIMAXを導入
      mini_value()の時にαカットを検討
      max2_value()の時にβカットを検討
      mini2_value()の時にαカットを検討
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
        # if actionables == 0:
        #     raise Exception("アクションできません")
        raw_game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }
        action = self._choice(game)

        # ゲーム情報を元に戻す
        self.setting_game(game, raw_game_info)
        next_player_id, actionables, is_game_over = game.step(action, self.player_id)

        # debug
        self.count_list.append(self.count)
        self.time_list.append(time.time() - start_time)
        self.total_count += self.count
        self.count = 0

        return next_player_id, actionables, is_game_over

    def setting_game(self, game, game_info):
        game.black_board = game_info["black_board"]
        game.white_board = game_info["white_board"]
        game.action_player_id = game_info["action_player_id"]
        game.is_game_over = game_info["is_game_over"]
        game.turn = game_info["turn"]
        game.black_count = game_info["black_count"]
        game.white_count = game_info["white_count"]
    
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

        search_depth = 1  # 探索深さ

        game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }
        actionables_list.reverse()
        for action in actionables_list:
            self.setting_game(game, game_info)
            next_player_id, next_actionables, next_is_game_over = game.step(action, self.player_id)

            self.count += 1

            # ゲームが終了した場合
            if next_is_game_over:
                return action
            
            if next_player_id == self.player_id:
                value = self._max_value(game, None, search_depth, next_actionables, next_player_id)
            else:
                value = self._min_value(game, max_value, search_depth, next_actionables, next_player_id)

            if value >= max_value:
                max_value = value
                max_action = action
            
            # if self.count > 500:
            #     return max_action
        
        return max_action

    def _min_value(self, game, alfa, search_depth, actionables, action_player_id):
        """
        最小値を返す
        """
        
        min_value = float("inf")  # 無限

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1
        
        search_depth += 1

        game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }
        actionables_list.reverse()
        for action in actionables_list:
            self.setting_game(game, game_info)
            next_player_id, next_actionables, next_is_game_over = game.step(action, action_player_id)
            
            self.count += 1

            if next_is_game_over:
                # 引き分けの時は0を返す
                if game.win_player == "2":
                    return 0
                else:
                    return float("-inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(game)
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(game, min_value, search_depth, next_actionables, next_player_id)
                else:
                    value = self._min_value(game, None, search_depth, next_actionables, next_player_id)

            if value < min_value:
                min_value = value
            
            # αカット
            if alfa is not None and min_value < alfa:
                return min_value
        
        return min_value

    def _max_value(self, game, beta, search_depth, actionables, action_player_id):
        """
        最大値を返す
        """
        
        max_value = float("-inf")  # マイナス無限

        actionables_list = []
        mask = 0x8000000000000000
        for i in range(64):
            if mask & actionables != 0:
                actionables_list.append(mask)
            mask = mask >> 1
        
        search_depth += 1  # 探索深さ

        game_info = {
            "black_board": game.black_board,
            "white_board": game.white_board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "turn": game.turn,
            "black_count": game.black_count,
            "white_count": game.white_count,
        }
        actionables_list.reverse()
        for action in actionables_list:
            self.setting_game(game, game_info)
            next_player_id, next_actionables, next_is_game_over = game.step(action, action_player_id)
            
            self.count += 1

            # 引き分けの時は0を返す
            if next_is_game_over:
                if game.win_player == "2":
                    return 0
                else:
                    return float("inf")
            
            # 状態の価値を計算
            if search_depth == 4:
                value = self._evaluate(game)
            else:
                if next_player_id == self.player_id:
                    value = self._max_value(game, None, search_depth, next_actionables, next_player_id)
                else:
                    value = self._min_value(game, max_value, search_depth, next_actionables, next_player_id)

            if value > max_value:
                max_value = value
            
            # βカット
            if beta is not None and max_value > beta:
                return max_value
        
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
          + b2,b7,g2,g7のどれかに自分の石がある場合 * -100
          + b2,b7,g2,g7のどれかに相手の石がある場合 * -100
        """

        black_count = game.black_count
        white_count = game.white_count
        black_corner_count = 0
        white_corner_count = 0
        black_near_corner_count = 0
        white_near_corner_count = 0
        black_edge_count = 0
        white_edge_count = 0
        result = 0

        if game.turn < 56:

            # 角の数を計算
            mask_corner = 0x8100000000000081
            black_corner_count = bin(game.black_board & mask_corner).count("1")
            white_corner_count = bin(game.white_board & mask_corner).count("1")

            # 角ちか
            mask_near_corner_ur = 0x0203000000000000
            mask_near_corner_ul = 0x40c0000000000000
            mask_near_corner_dr = 0x0000000000000302
            mask_near_corner_dl = 0x000000000000c040

            mask_corner_ur = 0x0100000000000000
            mask_corner_ul = 0x8000000000000000
            mask_corner_dr = 0x0000000000000001
            mask_corner_dl = 0x0000000000000080

            blank_board = ~(game.black_board | game.white_board)
            # 角が空白の時
            if mask_corner_ur & blank_board != 0:
                black_near_corner_count += bin(mask_near_corner_ur & game.black_board).count("1")
                white_near_corner_count += bin(mask_near_corner_ur & game.white_board).count("1")
            if mask_corner_ul & blank_board != 0:
                black_near_corner_count += bin(mask_near_corner_ul & game.black_board).count("1")
                white_near_corner_count += bin(mask_near_corner_ul & game.white_board).count("1")
            if mask_corner_dr & blank_board != 0:
                black_near_corner_count += bin(mask_near_corner_dr & game.black_board).count("1")
                white_near_corner_count += bin(mask_near_corner_dr & game.white_board).count("1")
            if mask_corner_dl & blank_board != 0:
                black_near_corner_count += bin(mask_near_corner_dl & game.black_board).count("1")
                white_near_corner_count += bin(mask_near_corner_dl & game.white_board).count("1")

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
                result += black_near_corner_count * -100
                result += white_near_corner_count * 100
                result += black_edge_count * 10
                result += white_edge_count * -10
            elif self.player_id == "0":
                result += black_count * -1
                result += white_count * 1
                result += black_corner_count * -100
                result += white_corner_count * 100
                result += white_near_corner_count * -100
                result += black_near_corner_count * 100
                result += black_edge_count * -10
                result += white_edge_count * 10
            else:
                logger.error("不正なプレイヤーIDです")
        
        elif game.turn <=60:
            if self.player_id == "1":
                result += (black_count - white_count)*100
            elif self.player_id == "0":
                result += (white_count - black_count)*100

        return result 
    
    



import logging
import itertools


logging.basicConfig(level=logging.INFO, format='%(message)s')  # ここでログレベルを設定する(debug<info<warning<error)
logger = logging.getLogger(__name__)


class Game():
    def __init__(self, game_info=None):
        """
        ゲームの初期化
            boardの表記
                0 1 2 3 4 5 6 7 
              0 - - - - - - - -
              1 - - - - - - - -
              2 - - - - - - - -
              3 - - - - - - - -
              4 - - - - - - - -
              5 - - - - - - - -
              6 - - - - - - - -
              7 - - - - - - - -
            
            ※ codingameでの表記
                a b c d e f g h
              1 - - - - - - - -
              2 - - - - - - - -
              3 - - - - - - - -
              4 - - - - - - - -
              5 - - - - - - - -
              6 - - - - - - - -
              7 - - - - - - - -
              8 - - - - - - - -

            boardの保存方法
              -> 2次元配列

            ※ codingameでのboardの保存方法
              -> 1次元配列            
        """
        if game_info is not None:
            self.black_board = game_info["black_board"]
            self.white_board = game_info["white_board"]
            self.action_player_id = game_info["action_player_id"]
            self.is_game_over = game_info["is_game_over"]
            self.win_player = game_info["win_player"]
            self.turn = game_info["turn"]
            self.black_count = game_info["black_count"]
            self.white_count = game_info["white_count"]
        else:
            self.black_board = 0x0000000810000000
            self.white_board = 0x0000001008000000
            self.action_player_id = "1"  # "1": 先行(黒)、"0": 後攻(白)
            self.is_game_over = False
            self.win_player = ""  # "1": 先行(黒)の勝ち、"0": 後攻(白)の勝ち、"2": 引き分け
            self.turn = 0  # ターン数
            logger.debug("ゲームを開始します")
            # self.print_board()
            self.black_count = 2
            self.white_count = 2
    
    def print_board(self):
        """
        ボードの状態を出力
        """
        white_board_str = bin(self.white_board)[2:].zfill(64)  # 64bitの文字列に変換
        black_board_str = bin(self.black_board)[2:].zfill(64)
        result = ""
        # print(len(white_board_str), len(black_board_str))
        for i in range(64):
            if white_board_str[i] == "1":
                result += "0"
            elif black_board_str[i] == "1":
                result += "1"
            else:
                result += "."
            if i % 8 == 7:
                result += "\n"
        
        logger.info(f"---{self.turn}回目---\n{result}\n")

            

    def step(self, action, player_id):
        """ 
        アクション

        Return:
            next_player_id: 次アクション可能なプレイヤーのID
            actionables: 次アクション可能なリスト
            is_game_over: ゲームが終了したかどうか
        """
        # アクション可能か(速度節約のため)
        # if not self.is_actionable(action, player_id):
        #     logger.error(
        #         "プレイヤーID: %s\nアクション: %s\n可能なアクション: %s",
        #         player_id, action, self.get_actionables(player_id)
        #     )
        #     raise Exception("不正なアクションです")

        # アクションを実行
        self.set_board(action, player_id)

        # 石の数を更新
        
        self.black_count = bin(self.black_board).count("1")
        self.white_count = bin(self.white_board).count("1")

        self.turn += 1

        # self.print_board()

        # ゲームが終了かどうか
        is_game_over = self.check_game_over()
        if is_game_over:
            return "", 0x0, True

        # 次アクション可能なリストを取得
        next_player_id = "0" if self.action_player_id=="1" else "1"
        actionables = self.get_actionables(next_player_id)
        
        # 次のアクション可能なプレイヤーを更新
        if actionables == 0:
            actionables = self.get_actionables(self.action_player_id)
        else:
            self.action_player_id = next_player_id

        return self.action_player_id, actionables, False

    def set_board(self, action, player_id):
        """
        ボードの更新
        """
        mask_lr = 0x7e7e7e7e7e7e7e7e
        mask_ud = 0x00ffffffffffff00
        mask_lu_ru_ld_rd = 0x007e7e7e7e7e7e00

        reverse = 0x0000000000000000

        # 石を置く
        if player_id == "1":
            mask_left = mask_lr & self.white_board  # 左方向
            mask_right = mask_lr & self.white_board
            mask_up = mask_ud & self.white_board
            mask_down = mask_ud & self.white_board
            mask_left_up = mask_lu_ru_ld_rd & self.white_board
            mask_right_up = mask_lu_ru_ld_rd & self.white_board
            mask_left_down = mask_lu_ru_ld_rd & self.white_board
            mask_right_down = mask_lu_ru_ld_rd & self.white_board

            l_rev = (action << 1) & mask_left
            r_rev = (action >> 1) & mask_right
            u_rev = (action << 8) & mask_up
            d_rev = (action >> 8) & mask_down
            lu_rev = (action << 7) & mask_left_up
            ru_rev = (action << 9) & mask_right_up
            ld_rev = (action >> 9) & mask_left_down
            rd_rev = (action >> 7) & mask_right_down

            for i in range(5):
                l_rev |= (l_rev << 1) & mask_left
                r_rev |= (r_rev >> 1) & mask_right
                u_rev |= (u_rev << 8) & mask_up
                d_rev |= (d_rev >> 8) & mask_down
                lu_rev |= (lu_rev << 7) & mask_left_up
                ru_rev |= (ru_rev << 9) & mask_right_up
                ld_rev |= (ld_rev >> 9) & mask_left_down
                rd_rev |= (rd_rev >> 7) & mask_right_down
    
            if (l_rev << 1) & self.black_board != 0:
                reverse |= l_rev
            if (r_rev >> 1) & self.black_board != 0:
                reverse |= r_rev
            if (u_rev << 8) & self.black_board != 0:
                reverse |= u_rev
            if (d_rev >> 8) & self.black_board != 0:
                reverse |= d_rev
            if (lu_rev << 7) & self.black_board != 0:
                reverse |= lu_rev
            if (ru_rev << 9) & self.black_board != 0:
                reverse |= ru_rev
            if (ld_rev >> 9) & self.black_board != 0:
                reverse |= ld_rev
            if (rd_rev >> 7) & self.black_board != 0:
                reverse |= rd_rev

            self.black_board |= (action | reverse)
            self.white_board ^= reverse
        
        elif player_id == "0":
            mask_left = mask_lr & self.black_board  # 左方向
            mask_right = mask_lr & self.black_board
            mask_up = mask_ud & self.black_board
            mask_down = mask_ud & self.black_board
            mask_left_up = mask_lu_ru_ld_rd & self.black_board
            mask_right_up = mask_lu_ru_ld_rd & self.black_board
            mask_left_down = mask_lu_ru_ld_rd & self.black_board
            mask_right_down = mask_lu_ru_ld_rd & self.black_board

            l_rev = (action << 1) & mask_left
            r_rev = (action >> 1) & mask_right
            u_rev = (action << 8) & mask_up
            d_rev = (action >> 8) & mask_down
            lu_rev = (action << 7) & mask_left_up
            ru_rev = (action << 9) & mask_right_up
            ld_rev = (action >> 9) & mask_left_down
            rd_rev = (action >> 7) & mask_right_down

            for i in range(5):
                l_rev |= (l_rev << 1) & mask_left
                r_rev |= (r_rev >> 1) & mask_right
                u_rev |= (u_rev << 8) & mask_up
                d_rev |= (d_rev >> 8) & mask_down
                lu_rev |= (lu_rev << 7) & mask_left_up
                ru_rev |= (ru_rev << 9) & mask_right_up
                ld_rev |= (ld_rev >> 9) & mask_left_down
                rd_rev |= (rd_rev >> 7) & mask_right_down
            
            if (l_rev << 1) & self.white_board != 0:
                reverse |= l_rev
            if (r_rev >> 1) & self.white_board != 0:
                reverse |= r_rev
            if (u_rev << 8) & self.white_board != 0:
                reverse |= u_rev
            if (d_rev >> 8) & self.white_board != 0:
                reverse |= d_rev
            if (lu_rev << 7) & self.white_board != 0:
                reverse |= lu_rev
            if (ru_rev << 9) & self.white_board != 0:
                reverse |= ru_rev
            if (ld_rev >> 9) & self.white_board != 0:
                reverse |= ld_rev
            if (rd_rev >> 7) & self.white_board != 0:
                reverse |= rd_rev

            self.white_board |= (action | reverse)
            self.black_board ^= reverse
        else:
            logger.error("不正なプレイヤーIDです")

    def get_actionables(self, player_id):
        """
        可能なアクションを返却

        処理:
          1. 左方向に対してい置ける場所を取得
          2. 右方向に対してい置ける場所を取得
          3. 上方向に対してい置ける場所を取得
          4. 下方向に対してい置ける場所を取得
          5. 左上方向に対してい置ける場所を取得
          6. 右上方向に対してい置ける場所を取得
          7. 左下方向に対してい置ける場所を取得
          8. 右下方向に対してい置ける場所を取得
        """
        mask_lr = 0x7e7e7e7e7e7e7e7e
        mask_ud = 0x00ffffffffffff00
        mask_lu_ru_ld_rd = 0x007e7e7e7e7e7e00

        # 空白の場所
        blank_board = ~(self.black_board | self.white_board)


        if player_id == "1":
            # 1. 左方向に対してい置ける場所を取得
            white_lr_mask = self.white_board & mask_lr  # 列1-6かつ白の場所
            white_ud_mask = self.white_board & mask_ud
            white_mask_lu_ru_ld_rd = self.white_board & mask_lu_ru_ld_rd

            l_white = (self.black_board << 1) & white_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
            r_white = (self.black_board >> 1) & white_lr_mask
            u_white = (self.black_board << 8) & white_ud_mask
            d_white = (self.black_board >> 8) & white_ud_mask
            lu_white = (self.black_board << 9) & white_mask_lu_ru_ld_rd
            ru_white = (self.black_board << 7) & white_mask_lu_ru_ld_rd
            ld_white = (self.black_board >> 7) & white_mask_lu_ru_ld_rd
            rd_white = (self.black_board >> 9) & white_mask_lu_ru_ld_rd

            for i in range(5):
                l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
                r_white |= (r_white >> 1) & white_lr_mask
                u_white |= (u_white << 8) & white_ud_mask
                d_white |= (d_white >> 8) & white_ud_mask
                lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
                ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
                ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
                rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

            legal_left = (l_white << 1) & blank_board
            legal_right = (r_white >> 1) & blank_board
            legal_up = (u_white << 8) & blank_board
            legal_down = (d_white >> 8) & blank_board
            legal_lu = (lu_white << 9) & blank_board
            legal_ru = (ru_white << 7) & blank_board
            legal_ld = (ld_white >> 7) & blank_board
            legal_rd = (rd_white >> 9) & blank_board
        elif player_id == "0":
            # 1. 左方向に対してい置ける場所を取得
            black_lr_mask = self.black_board & mask_lr  # 列1-6かつ白の場所
            black_ud_mask = self.black_board & mask_ud
            black_mask_lu_ru_ld_rd = self.black_board & mask_lu_ru_ld_rd

            l_black = (self.white_board << 1) & black_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
            r_black = (self.white_board >> 1) & black_lr_mask
            u_black = (self.white_board << 8) & black_ud_mask
            d_black = (self.white_board >> 8) & black_ud_mask
            lu_black = (self.white_board << 9) & black_mask_lu_ru_ld_rd
            ru_black = (self.white_board << 7) & black_mask_lu_ru_ld_rd
            ld_black = (self.white_board >> 7) & black_mask_lu_ru_ld_rd
            rd_black = (self.white_board >> 9) & black_mask_lu_ru_ld_rd

            for i in range(5):
                l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
                r_black |= (r_black >> 1) & black_lr_mask
                u_black |= (u_black << 8) & black_ud_mask
                d_black |= (d_black >> 8) & black_ud_mask
                lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
                ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
                ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
                rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

            legal_left = (l_black << 1) & blank_board
            legal_right = (r_black >> 1) & blank_board
            legal_up = (u_black << 8) & blank_board
            legal_down = (d_black >> 8) & blank_board
            legal_lu = (lu_black << 9) & blank_board
            legal_ru = (ru_black << 7) & blank_board
            legal_ld = (ld_black >> 7) & blank_board
            legal_rd = (rd_black >> 9) & blank_board
        else:
            logger.error("不正なプレイヤーIDです")

        # 9. 1-8の合計
        legal = legal_left | legal_right | legal_up | legal_down | legal_lu | legal_ru | legal_ld | legal_rd

        return legal

    def is_actionable(self, action, player_id):
        """
        アクション可能か判定
        """
        # アクション待ちのプレイヤーかどうか
        if self.action_player_id != player_id:
            logger.info("アクション待ちのプレイヤーではありません")
            return False 
        
        # ゲームが終了しているかどうか
        if self.is_game_over:
            logger.info("ゲームは終了しています")
            return False 

        # 可能なアクションの手かどうか
        actionable_list = self.get_actionables(player_id)
        if action not in actionable_list:
            logger.error("不可能なアクションです: ")
            return False 

        return True
    
    def check_game_over(self):
        """
        ゲームが終了したかどうかを判定
        """
        result = False

        # どちらかの石が0個になった場合
        if self.black_count == 0:
            self.win_player = "0"
            self.is_game_over = True
            return True
        elif self.white_count == 0:
            self.win_player = "1"
            self.is_game_over = True
            return True
        
        # 両者ともアクションできない場合
        black_actionables = self.get_actionables("1")
        
        # 光速かのため追加
        if black_actionables != 0:
            return False

        white_actionables = self.get_actionables("0")
        if black_actionables == 0 and white_actionables == 0:
            result = True
            self.is_game_over = True
            if self.black_count > self.white_count:
                self.win_player = "1"
            elif self.black_count < self.white_count:
                self.win_player = "0"
            else:
                self.win_player = "2"
        
        return result

    def get_result(self):
        """
        ゲームの勝敗を取得
        """
        result = {
            "win_player": "",
            "black_count": 0,
            "white_count": 0,
            "turn": 0
        }

        if self.is_game_over:
            result["win_player"] = self.win_player
            result["turn"] = self.turn
            result["black_count"] = self.black_count
            result["white_count"] = self.white_count
        
        return result



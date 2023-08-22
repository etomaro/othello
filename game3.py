"""
ゲーム疑似クラスで次のアクションプレイヤー判定、ゲーム終了判定などの機能を削除(高速化とnegamaxで使いやすいように)
"""
import time
from functools import lru_cache



def get_game_init():
    """
    ゲームの初期化
    """

    black_board = 0x0000000810000000
    white_board = 0x0000001008000000
    actionables = 0x0000102004080000

    return black_board, white_board, actionables


@lru_cache()
def get_actionables(player_id, black_board, white_board):
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
    blank_board = ~(black_board | white_board)


    if player_id == 1:
        # 1. 左方向に対してい置ける場所を取得
        white_lr_mask = white_board & mask_lr  # 列1-6かつ白の場所
        white_ud_mask = white_board & mask_ud
        white_mask_lu_ru_ld_rd = white_board & mask_lu_ru_ld_rd

        l_white = (black_board << 1) & white_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
        r_white = (black_board >> 1) & white_lr_mask
        u_white = (black_board << 8) & white_ud_mask
        d_white = (black_board >> 8) & white_ud_mask
        lu_white = (black_board << 9) & white_mask_lu_ru_ld_rd
        ru_white = (black_board << 7) & white_mask_lu_ru_ld_rd
        ld_white = (black_board >> 7) & white_mask_lu_ru_ld_rd
        rd_white = (black_board >> 9) & white_mask_lu_ru_ld_rd

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

        l_white |= (l_white << 1) & white_lr_mask  # 上記に当てはまる場所(l_white)かつ1つ左の白かつ列1-6の場所(white_lr_maskに当てはまる箇所)を追加
        r_white |= (r_white >> 1) & white_lr_mask
        u_white |= (u_white << 8) & white_ud_mask
        d_white |= (d_white >> 8) & white_ud_mask
        lu_white |= (lu_white << 9) & white_mask_lu_ru_ld_rd
        ru_white |= (ru_white << 7) & white_mask_lu_ru_ld_rd
        ld_white |= (ld_white >> 7) & white_mask_lu_ru_ld_rd
        rd_white |= (rd_white >> 9) & white_mask_lu_ru_ld_rd

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
    elif player_id == 0:
        # 1. 左方向に対してい置ける場所を取得
        black_lr_mask = black_board & mask_lr  # 列1-6かつ白の場所
        black_ud_mask = black_board & mask_ud
        black_mask_lu_ru_ld_rd = black_board & mask_lu_ru_ld_rd

        l_black = (white_board << 1) & black_lr_mask  # 黒の1つ左の場所かつ列1-6かつ白の場所
        r_black = (white_board >> 1) & black_lr_mask
        u_black = (white_board << 8) & black_ud_mask
        d_black = (white_board >> 8) & black_ud_mask
        lu_black = (white_board << 9) & black_mask_lu_ru_ld_rd
        ru_black = (white_board << 7) & black_mask_lu_ru_ld_rd
        ld_black = (white_board >> 7) & black_mask_lu_ru_ld_rd
        rd_black = (white_board >> 9) & black_mask_lu_ru_ld_rd

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

        l_black |= (l_black << 1) & black_lr_mask  # 上記に当てはまる場所(l_black)かつ1つ左の白かつ列1-6の場所(black_lr_maskに当てはまる箇所)を追加
        r_black |= (r_black >> 1) & black_lr_mask
        u_black |= (u_black << 8) & black_ud_mask
        d_black |= (d_black >> 8) & black_ud_mask
        lu_black |= (lu_black << 9) & black_mask_lu_ru_ld_rd
        ru_black |= (ru_black << 7) & black_mask_lu_ru_ld_rd
        ld_black |= (ld_black >> 7) & black_mask_lu_ru_ld_rd
        rd_black |= (rd_black >> 9) & black_mask_lu_ru_ld_rd

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

    # 9. 1-8の合計
    legal = legal_left | legal_right | legal_up | legal_down | legal_lu | legal_ru | legal_ld | legal_rd

    return legal

@lru_cache()
def set_board(action, player_id, black_board, white_board):
    """
    ボードの更新
    """
    mask_lr = 0x7e7e7e7e7e7e7e7e
    mask_ud = 0x00ffffffffffff00
    mask_lu_ru_ld_rd = 0x007e7e7e7e7e7e00

    reverse = 0x0000000000000000

    # 石を置く
    if player_id == 1:
        mask_left = mask_lr & white_board  # 左方向
        mask_right = mask_lr & white_board
        mask_up = mask_ud & white_board
        mask_down = mask_ud & white_board
        mask_left_up = mask_lu_ru_ld_rd & white_board
        mask_right_up = mask_lu_ru_ld_rd & white_board
        mask_left_down = mask_lu_ru_ld_rd & white_board
        mask_right_down = mask_lu_ru_ld_rd & white_board

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

        if (l_rev << 1) & black_board != 0:
            reverse |= l_rev
        if (r_rev >> 1) & black_board != 0:
            reverse |= r_rev
        if (u_rev << 8) & black_board != 0:
            reverse |= u_rev
        if (d_rev >> 8) & black_board != 0:
            reverse |= d_rev
        if (lu_rev << 7) & black_board != 0:
            reverse |= lu_rev
        if (ru_rev << 9) & black_board != 0:
            reverse |= ru_rev
        if (ld_rev >> 9) & black_board != 0:
            reverse |= ld_rev
        if (rd_rev >> 7) & black_board != 0:
            reverse |= rd_rev

        black_board |= (action | reverse)
        white_board ^= reverse
    
    elif player_id == 0:
        mask_left = mask_lr & black_board  # 左方向
        mask_right = mask_lr & black_board
        mask_up = mask_ud & black_board
        mask_down = mask_ud & black_board
        mask_left_up = mask_lu_ru_ld_rd & black_board
        mask_right_up = mask_lu_ru_ld_rd & black_board
        mask_left_down = mask_lu_ru_ld_rd & black_board
        mask_right_down = mask_lu_ru_ld_rd & black_board

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
        
        if (l_rev << 1) & white_board != 0:
            reverse |= l_rev
        if (r_rev >> 1) & white_board != 0:
            reverse |= r_rev
        if (u_rev << 8) & white_board != 0:
            reverse |= u_rev
        if (d_rev >> 8) & white_board != 0:
            reverse |= d_rev
        if (lu_rev << 7) & white_board != 0:
            reverse |= lu_rev
        if (ru_rev << 9) & white_board != 0:
            reverse |= ru_rev
        if (ld_rev >> 9) & white_board != 0:
            reverse |= ld_rev
        if (rd_rev >> 7) & white_board != 0:
            reverse |= rd_rev

        white_board |= (action | reverse)
        black_board ^= reverse
    
    return black_board, white_board

def get_game_info(black_board, white_board):
    """
    黒の石の数
    白の石の数
    勝者: 0->後攻, 1->先行, 2->引き分け, 3->ゲーム中
    """
    black_count = bin(black_board).count("1")
    white_count = bin(white_board).count("1")

    black_actionables = get_actionables(1, black_board, white_board)
    white_actionables = get_actionables(0, black_board, white_board)

    if bin(black_actionables).count("1") == 0 and bin(white_actionables).count("1") == 0:
        if black_count < white_count:
            win_player = 0
        elif black_count > white_count:
            win_player = 1
        else:
            win_player = 2
    else:
        win_player = 3

    return black_count, white_count, win_player

def print_board(black_board, white_board):
    black_board = bin(black_board)[2:].zfill(64)
    white_board = bin(white_board)[2:].zfill(64)

    result = ""
    for i in range(64):
        if i % 8 == 0:
            result += "\n"
        if black_board[i] == "1":
            result += "○"
        elif white_board[i] == "1":
            result += "●"
        else:
            result += "-"
    
    print(result + "\n")
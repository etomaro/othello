"""
クラスでゲームオブジェクトを持つことを廃止したバージョン
"""
from functools import lru_cache


def get_game_init():
    """
    ゲームの初期化
    """
    game_info = {
        "black_board": 0x0000000810000000,
        "white_board": 0x0000001008000000,
        "action_player_id": "1",  # "1": 先行(黒)、"0": 後攻(白)
        "is_game_over": False,
        "win_player": "",  # "1": 先行(黒)の勝ち、"0": 後攻(白)の勝ち、"2": 引き分け
        "turn": 0,  # ターン数
        "black_count": 2,
        "white_count": 2
    }
    return game_info

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


    if player_id == "1":
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
    elif player_id == "0":
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
def is_actionable(action, player_id, my_player_id, black_board, white_board, is_game_over):
    """
    アクション可能か判定
    """
    # アクション待ちのプレイヤーかどうか
    if my_player_id != player_id:
        return False 
    
    # ゲームが終了しているかどうか
    if is_game_over:
        return False 

    # 可能なアクションの手かどうか
    actionable_list = get_actionables(player_id, black_board, white_board)
    if action not in actionable_list:
        return False 

    return True

@lru_cache()
def check_game_over(black_count, white_count, black_board, white_board):
    """
    ゲームが終了したかどうかを判定
    Returns:
        is_game_over: ゲームが終了したかどうか
        win_player: 勝利したプレイヤー
    """
    result = False
    win_player = ""

    # どちらかの石が0個になった場合
    if black_count == 0:
        return True, "0"
    elif white_count == 0:
        return True, "1"
    
    # 両者ともアクションできない場合
    black_actionables = get_actionables("1", black_board, white_board)
    
    # 光速かのため追加
    if black_actionables != 0:
        return False, ""

    white_actionables = get_actionables("0", black_board, white_board)
    if black_actionables == 0 and white_actionables == 0:
        result = True
        if black_count > white_count:
            win_player = "1"
        elif black_count < white_count:
            win_player = "0"
        else:
            win_player = "2"
    
    return result, win_player

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
    if player_id == "1":
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
    
    elif player_id == "0":
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

@lru_cache()
def step(action, black_board, white_board, action_player_id):
    """ 
    アクション

    0.01秒早くするためにlru_cacheを使ったため引数にturnが来るはずが消した
    stepした後にturn+=1をする必要あり

    Return:
        next_action_player_id
        actionables: 次アクション可能なリスト
        is_next_game_over: ゲームが終了したかどうか
        game_info: 次のゲーム情報
    """

    # アクションを実行
    next_black_board, next_white_board = set_board(action, action_player_id, black_board, white_board)

    # 石の数を更新
    
    next_black_count = bin(next_black_board).count("1")
    next_white_count = bin(next_white_board).count("1")

    # ゲームが終了かどうか
    is_next_game_over, win_player = check_game_over(
        next_black_count, next_white_count, next_black_board, next_white_board
    )
    if is_next_game_over:
        end_game_info = {
            "black_board": next_black_board,
            "white_board": next_white_board,
            "black_count": next_black_count,
            "white_count": next_white_count,
            "turn": "",
            "action_player_id": "",
            "win_player": win_player,
            "is_game_over": True
        }
        return "", 0x0, True, end_game_info

    # 次アクション可能なリストを取得
    next_player_id = "0" if action_player_id=="1" else "1"
    actionables = get_actionables(next_player_id, next_black_board, next_white_board)
    
    # 次のアクション可能なプレイヤーを更新
    if actionables == 0:
        actionables = get_actionables(action_player_id, next_black_board, next_white_board)
        next_action_player_id = action_player_id
    else:
        next_action_player_id = next_player_id
    
    next_game_info = {
        "black_board": next_black_board,
        "white_board": next_white_board,
        "black_count": next_black_count,
        "white_count": next_white_count,
        "turn": "",
        "action_player_id": next_action_player_id,
        "win_player": "",
        "is_game_over": False
    }

    return next_action_player_id, actionables, False, next_game_info

def get_actionables_list(actionables):
    actionables_list = []
    mask = 0x8000000000000000
    for i in range(64):
        if mask & actionables != 0:
            actionables_list.append(mask)
        mask = mask >> 1
    return actionables_list
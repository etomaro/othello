from game2 import *
import numpy as np
import time


def re_get_actionables(board):
    """
    board
      0x黒 + 0x白
    
    Return
       actionables
       num_actionables
    """
    black_board, white_board = board.split("-")

    black_board = int(black_board, 16)
    white_board = int(white_board, 16)

    print("black_board: ", hex(black_board))
    print("white_board: ", hex(white_board))

    actionables = get_actionables("1", black_board, white_board)

    num_actionables = bin(actionables).count("1")

    return actionables, num_actionables

def get_board(black_board, white_board):
    """
    black_board, white_boardから
    black_board + "-" + white_boardを返す
    """
    return hex(black_board) + "-" + hex(white_board)


def main():

    black_init_board = 0x0000000810000000
    white_init_board = 0x0000001008000000

    actionables = get_actionables("1", black_init_board, white_init_board)
    actionables_list = get_actionables_list(actionables)

    board = get_board(black_init_board, white_init_board)

    # turn
    n = 1

    # 調べたい値
    state_list = []
    state_list.append(board)
    state_obj = {}
    next_end_state_list = []
    # ループで必要な値
    next_state_list = []
    state_game_obj = {board: {
        "next_actionables": actionables_list,
        "next_action_player_id": "1",
        "black_board": black_init_board,
        "white_board": white_init_board
    }}
    next_state_game_obj = {}  # {next_board: {next_action_player_id: "", next_actionables: "", next_is_game_over: "", next_game_info: {}}}の形式

    state_time = time.time()
    while True:
        for board in state_list:
            actionables_list = state_game_obj[board]["next_actionables"]
            action_player_id = state_game_obj[board]["next_action_player_id"]
            black_board = state_game_obj[board]["black_board"]
            white_board = state_game_obj[board]["white_board"]

            for action in actionables_list:
                next_action_player_id , next_actionables, next_is_game_over, next_game_info = step(
                    action,
                    black_board, white_board, action_player_id
                )

                next_board = get_board(next_game_info["black_board"], next_game_info["white_board"])

                is_match = symmetry(next_board, next_state_list)
                if is_match:
                    continue
                else:
                    if board not in state_obj:
                        state_obj[board] = {}
                    state_obj[board][hex(action)] = next_board

                    if next_is_game_over:
                        next_end_state_list.append(next_board)
                    else:
                        next_state_list.append(next_board)
                        next_state_game_obj[next_board] = {
                            "next_actionables": get_actionables_list(next_actionables),
                            "next_action_player_id": next_action_player_id,
                            "black_board": next_game_info["black_board"],
                            "white_board": next_game_info["white_board"]
                        }
        
        # debug
        print("turn: ", n)
        print("経過時間: ", time.time() - state_time)
        # print("state_obj: ", state_obj)
        # print("next_state_list: ", next_state_list)
        print("num next_state_list: ", len(next_state_list))
        print("num next_end_state: ", len(next_end_state_list))
        print("\n")


        # 初期化
        n+=1
        if n == 11:
            break
        
        state_list = next_state_list
        next_state_list = []
        state_obj = {}
        state_game_obj = next_state_game_obj
        next_state_game_obj = {}
        next_end_state_list = []

def print_state(board):
    """
    board: 黒 + "-"+ 白
    
    """
    black_board, white_board = board.split("-")

    black_board, white_board = int(black_board, 16), int(white_board, 16)

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

    print(f"{result}\n")

def print_board_64(board):
    """
    black, white_boardのどちらか
    """
    board = bin(board)[2:].zfill(64)

    result = ""
    for i in range(64):
        if i % 8 == 0:
            result += "\n"
        if board[i] == "1":
            result += "○"
        else:
            result += "-"
    print(f"{result}\n")

def print_board_array(board):
    """
    2次元配列からboardを出力
    """
    result = ""
    for i in range(8):
      for j in range(8):
        result += board[i][j]
      result += "\n"
    print(result)
  
def symmetry(board, state_n_list):
    """
    board: 黒 + "-"+ 白
    state_n_list: turn=nの時のstateのリスト(n-1のstateに依存しない)

    Return 
        is_match: 対称したものが存在すればTrue
        black_board
        white_board

    1. 半時計に90度回転
    2. 半時計に180度回転
    3. 半時計に270度回転
    4. 左右反転
    5. 上下反転
    6. 左上から右下への対角線に関して対称
    7. 右上から左下への対角線に関して対称
    """
    black_board, white_board = board.split("-")

    black_board, white_board = int(black_board, 16), int(white_board, 16)

    black_board = bin(black_board)[2:].zfill(64)
    white_board = bin(white_board)[2:].zfill(64)

    # 8*8の2次元配列を初期化
    board_array = [[0 for i in range(8)] for j in range(8)]
    for i in range(64):
      if black_board[i] == "1":
          board_array[i//8][i%8] = "1"
      elif white_board[i] == "1":
          board_array[i//8][i%8] = "0"
      else:
          board_array[i//8][i%8] = "-"

    # 1. 半時計に90度回転
    board_array_90 = np.rot90(board_array, 1)
    # 2. 半時計に180度回転
    board_array_180 = np.rot90(board_array, 2)
    # 3. 半時計に270度回転
    board_array_270 = np.rot90(board_array, 3)
    # 4. 左右反転
    board_array_lr = np.fliplr(board_array)
    # 5. 上下反転
    board_array_ud = np.flipud(board_array)
    # 6. 左上から右下への対角線に関して対称
    # 7. 右上から左下への対角線に関して対称
    board_array_dia1 = [[0 for i in range(8)] for j in range(8)]
    board_array_dia2 = [[0 for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            board_array_dia1[i][j] = board_array[j][i]
            board_array_dia2[i][j] = board_array[8 - j - 1][8 - i - 1]
    
    # debug
    # print("最初のボード")
    # print_board_array(board_array)
    # print("90度回転")
    # print_board_array(board_array_90)
    # print("180度回転")
    # print_board_array(board_array_180)
    # print("270度回転")
    # print_board_array(board_array_270)
    # print("左右反転")
    # print_board_array(board_array_lr)
    # print("上下反転")
    # print_board_array(board_array_ud)
    # print("左上から右下への対角線に関して対称")
    # print_board_array(board_array_dia1)
    # print("右上から左下への対角線に関して対称")
    # print_board_array(board_array_dia2)

    # 2次元配列からblack_blard+"-"+white_boardの形式に変換
    black_board_90, white_board_90 = "0b", "0b"
    black_board_180, white_board_180 = "0b", "0b"
    black_board_270, white_board_270 = "0b", "0b"
    black_board_lr, white_board_lr = "0b", "0b"
    black_board_ud, white_board_ud = "0b", "0b"
    black_board_dia1, white_board_dia1 = "0b", "0b"
    black_board_dia2, white_board_dia2 = "0b", "0b"

    for i in range(8):
        for j in range(8):
            # 90度回転
            if board_array_90[i][j] == "1":
                black_board_90 += "1"
                white_board_90 += "0"
            elif board_array_90[i][j] == "0":
                black_board_90 += "0"
                white_board_90 += "1"
            else:
                black_board_90 += "0"
                white_board_90 += "0"
            # 180度回転
            if board_array_180[i][j] == "1":
                black_board_180 += "1"
                white_board_180 += "0"
            elif board_array_180[i][j] == "0":
                black_board_180 += "0"
                white_board_180 += "1"
            else:
                black_board_180 += "0"
                white_board_180 += "0"
            # 270度回転
            if board_array_270[i][j] == "1":
                black_board_270 += "1"
                white_board_270 += "0"
            elif board_array_270[i][j] == "0":
                black_board_270 += "0"
                white_board_270 += "1"
            else:
                black_board_270 += "0"
                white_board_270 += "0"
            # 左右反転
            if board_array_lr[i][j] == "1":
                black_board_lr += "1"
                white_board_lr += "0"
            elif board_array_lr[i][j] == "0":
                black_board_lr += "0"
                white_board_lr += "1"
            else:
                black_board_lr += "0"
                white_board_lr += "0"
            # 上下反転
            if board_array_ud[i][j] == "1":
                black_board_ud += "1"
                white_board_ud += "0"
            elif board_array_ud[i][j] == "0":
                black_board_ud += "0"
                white_board_ud += "1"
            else:
                black_board_ud += "0"
                white_board_ud += "0"
            # 左上から右下への対角線に関して対称
            if board_array_dia1[i][j] == "1":
                black_board_dia1 += "1"
                white_board_dia1 += "0"
            elif board_array_dia1[i][j] == "0":
                black_board_dia1 += "0"
                white_board_dia1 += "1"
            else:
                black_board_dia1 += "0"
                white_board_dia1 += "0"
            # 右上から左下への対角線に関して対称
            if board_array_dia2[i][j] == "1":
                black_board_dia2 += "1"
                white_board_dia2 += "0"
            elif board_array_dia2[i][j] == "0":
                black_board_dia2 += "0"
                white_board_dia2 += "1"
            else:
                black_board_dia2 += "0"
                white_board_dia2 += "0"
    
    black_board_90 = hex(int(black_board_90, 2))
    white_board_90 = hex(int(white_board_90, 2))
    black_board_180 = hex(int(black_board_180, 2))
    white_board_180 = hex(int(white_board_180, 2))
    black_board_270 = hex(int(black_board_270, 2))
    white_board_270 = hex(int(white_board_270, 2))
    black_board_lr = hex(int(black_board_lr, 2))
    white_board_lr = hex(int(white_board_lr, 2))
    black_board_ud = hex(int(black_board_ud, 2))
    white_board_ud = hex(int(white_board_ud, 2))
    black_board_dia1 = hex(int(black_board_dia1, 2))
    white_board_dia1 = hex(int(white_board_dia1, 2))
    black_board_dia2 = hex(int(black_board_dia2, 2))
    white_board_dia2 = hex(int(white_board_dia2, 2))

    board_90 = black_board_90 + "-" + white_board_90
    board_180 = black_board_180 + "-" + white_board_180
    board_270 = black_board_270 + "-" + white_board_270
    board_lr = black_board_lr + "-" + white_board_lr
    board_ud = black_board_ud + "-" + white_board_ud
    board_dia1 = black_board_dia1 + "-" + white_board_dia1
    board_dia2 = black_board_dia2 + "-" + white_board_dia2

    # debug
    # print("最初のボード")
    # print_state(board)
    # print("90度回転")
    # print_state(board_90)
    # print("180度回転")
    # print_state(board_180)
    # print("270度回転")
    # print_state(board_270)
    # print("左右反転")
    # print_state(board_lr)
    # print("上下反転")
    # print_state(board_ud)
    # print("左上から右下への対角線に関して対称")
    # print_state(board_dia1)
    # print("右上から左下への対角線に関して対称")
    # print_state(board_dia2)
    # print("\n")

    is_match = False
    if board in state_n_list or board_90 in state_n_list or board_180 in state_n_list or board_270 in state_n_list or board_lr in state_n_list or board_ud in state_n_list or board_dia1 in state_n_list or board_dia2 in state_n_list:
        is_match = True
    
    return is_match

# def test_rotate(board):
#     for i in range(64):


if __name__ == "__main__":
    main()
    # symmetry("F000000000000000-0000001008000000")
    
        
        



    

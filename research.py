from game2 import *

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

def main():
    
    actionables1, num_actionables1 = "", 0
    actionables2, num_actionables2 = "", 0

    # {前のstateでのアクション: 次のstateでのアクション}
    state2 = {
        "": ""
    }

    state3 = {
        "": ""
    }

    num_state2 = 0
    num_state3 = 0

    black_init_board = 0x0000000810000000
    white_init_board = 0x0000001008000000

    actionables = get_actionables("1", black_init_board, white_init_board)

    actionables_list = get_actionables_list(actionables)

    for action in actionables_list:
        



    



if __name__ == "__main__":
    board = "0000000810000000-0000001008000000"
    actionables, num_actionables = re_get_actionables(board)
    print("actionables: ", hex(actionables))
    print("num_actionables: ", num_actionables)
    

from game3 import *
from player.minimax_v6v3v2 import MiniMaxV6V3V2Player

black_board = 0x3e3c3e1f5c646200
white_board = 0x0001c0e0a09a1038

# print_board(black_board, white_board)

actionables = get_actionables(0, black_board, white_board)

# print(actionables)

player = MiniMaxV6V3V2Player(0)
next_black_board, next_white_board = player.action(black_board, white_board, actionables)

print(next_black_board)
print(next_white_board)
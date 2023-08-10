from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from game import Game
from player.random import RandomPlayer
from player.firstModel import FirstModelPlayer
from player.minimax_v4 import MiniMaxV4Player
from player.minimax_v5 import MiniMaxV5Player

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://bitgame-eacc4.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/othello/models")
def start():
    
    models = ["random", "v1ai", "v2ai"]
    result = {"model": models}

    return result

@app.get("/othello/start")
def start():
    game = Game()

    actionables = encodeActionables(game.get_actionables(game.action_player_id))
    board = encodeBoard(game.white_board, game.black_board)
    result = {
        "game_info": {
            "board": board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "win_player": game.win_player,
            "turn": game.turn,
            "white_count": game.white_count,
            "black_count": game.black_count,
        },
        "actionables": actionables,
    }

    return result


class Info(BaseModel):
    game_info: dict
    action: list
    is_back_action: bool 
    action_model: str

@app.post("/othello/action")
def action(info: Info):
    info = info.dict()

    white_board, black_board = decodeBoard(info["game_info"]["board"])
    game_info = {
        "white_board": white_board,
        "black_board": black_board,
        "action_player_id": info["game_info"]["action_player_id"],
        "is_game_over": info["game_info"]["is_game_over"],
        "win_player": info["game_info"]["win_player"],
        "turn": info["game_info"]["turn"],
        "white_count": info["game_info"]["white_count"],
        "black_count": info["game_info"]["black_count"],
    }
    game = Game(game_info)

    # AIによるアクション
    if info["is_back_action"]:
        player = ""
        if info["action_model"] == "random":
            player = RandomPlayer(info["game_info"]["action_player_id"])
        elif info["action_model"] == "v1ai":
            player = MiniMaxV4Player(info["game_info"]["action_player_id"])
        elif info["action_model"] == "v2ai":
            player = MiniMaxV5Player(info["game_info"]["action_player_id"])

        next_player_id, actionables, is_game_over = player.action(game)
    else:
        action = decodeAction(info["action"])
        next_player_id, actionables, is_game_over = game.step(action, info["game_info"]["action_player_id"])
    
    actionables = encodeActionables(actionables)
    board = encodeBoard(game.white_board, game.black_board)

    result = {
        "game_info": {
            "board": board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "win_player": game.win_player,
            "turn": game.turn,
            "white_count": game.white_count,
            "black_count": game.black_count,
        },
        "actionables": actionables,
    }
    
    return result

def encodeBoard(white_board, black_board):
    """
    BitBoardから2次元配列に変換する
    white_board, black_boardからboardを生成する
    """
    board = [["" for i in range(8)] for j in range(8)]

    for i in range(8):
        for j in range(8):
            if white_board & (0x8000000000000000 >> (i * 8 + j)):
                board[i][j] = "0"
            elif black_board & (0x8000000000000000 >> (i * 8 + j)):
                board[i][j] = "1"
            else:
                board[i][j] = "."
    
    return board

def encodeActionables(actionables):
    """
    16進数64bitから2次元配列に変換する
    """
    result = []
    if actionables == 0x0000000000000000:
        return result
    for i in range(64):
        if actionables & (0x8000000000000000 >> i):
            result.append([i // 8, i % 8])
    
    return result


def decodeBoard(board):
    """
    2次元配列からBitBoardに変換する
    white_board, black_boardを生成する
    """
    white_board = 0x0000000000000000
    black_board = 0x0000000000000000

    for i in range(8):
        for j in range(8):
            if board[i][j] == "0":
                white_board |= (0x8000000000000000 >> (i * 8 + j))
            elif board[i][j] == "1":
                black_board |= (0x8000000000000000 >> (i * 8 + j))
    
    return white_board, black_board


def decodeAction(action):
    """
    配列から16進数64bitに変換する
    """
    result = 0x8000000000000000
    row = action[0]
    col = action[1]
    result = result >> (row * 8 + col)

    return result



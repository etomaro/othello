from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from game import Game
from player.random import RandomPlayer
from player.firstModel import FirstModelPlayer

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
    
    models = ["random", "v1ai"]
    result = {"model": models}

    return result

@app.get("/othello/start")
def start():
    game = Game()
    result = {
        "game_info": {
            "board": game.board,
            "action_player_id": game.action_player_id,
            "is_game_over": game.is_game_over,
            "win_player": game.win_player,
            "turn": game.turn,
            "white_count": game.white_count,
            "black_count": game.black_count,
        },
        "actionables": game.get_actionables(game.action_player_id),
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
    game_info = {
        "board": info["game_info"]["board"],
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
            player = FirstModelPlayer(info["game_info"]["action_player_id"])

        next_player_id, actionables, is_game_over = player.action(game)
    else:
        next_player_id, actionables, is_game_over = game.step(info["action"], info["game_info"]["action_player_id"])
    
    result = {
        "game_info": {
            "board": game.board,
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
from os.path import exists
import sys

if not exists("./.env"):
    print("[ERROR] .env not found. Did you install?")
    print("https://github.com/redigermany/cas-robocup-master/#install")
    sys.exit()

import asyncio
import random
import websockets
import jsonpickle
import threading
import datetime
import signal

from enum import Enum

import asyncio

from dotenv import dotenv_values
config = dotenv_values(".env")

from src.web.server import runWebserver

class EGameState(Enum):
    PLAYING = 1
    PAUSED = 2
    FOUL = 3
    ENDED = 4
    GOAL = 5

class GameState:
    state:EGameState = EGameState.PAUSED

class Singleton(object):
    _instance = None

    data = {
        "state": "debug",
        "time_remaining": "time_remaining",
        "robots": [],
        "balls": []
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def setBalls(self,balls):
        self.data["balls"] = balls

    def setRobots(self,robots):
        self.data["robots"] = robots

s1 = Singleton()
# {
#     "state": "debug",
#     "time_remaining": message,
#     "robots": [
#         {
#             "x": random.random(),
#             "y": random.random(),
#             "id": "blue",
#             "angle": random.random()*360,
#         },
#         {
#             "x": random.random(),
#             "y": random.random(),
#             "id": "green",
#             "angle": random.random()*360,
#         },
#         {
#             "x": random.random(),
#             "y": random.random(),
#             "id": "yellow",
#             "angle": random.random()*360,
#         },
#         {
#             "x": random.random(),
#             "y": random.random(),
#             "id": "pink",
#             "angle": random.random()*360,
#         }
#     ],
#     "balls": [
#         {
#             "x": random.random(),
#             "y": random.random(),
#         }     
#     ]
# }

async def establishConnection():
    WS_PORT = config.get("WS_PORT")
    WS_HOST = "localhost"
    if(len(sys.argv)>1):
        print(sys.argv)
        WS_HOST = sys.argv[1]
    async with websockets.connect(f"ws://{WS_HOST}:{WS_PORT}") as websocket:
        print(f"Connected to {WS_HOST}:{WS_PORT}")
        message = websocket.recv()
    

        async for message in websocket:
            print(f"Received: {message}")


if __name__ == "__main__":
   asyncio.run(establishConnection())
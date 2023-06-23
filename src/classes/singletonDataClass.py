#from enum import Enum
from datetime import datetime

# class EGameState(Enum):
#     PLAYING = 1
#     PAUSED = 2
#     FOUL = 3
#     ENDED = 4
#     GOAL = 5

# class GameState:
#     state:EGameState = EGameState.PAUSED

class Singleton(object):
    _instance = None

    data = {
        "time": "time",
        "state": "debug",
        "teams": [
            {
                "name": "Up",
                "score": 0
            },
            {
                "name": "Down",
                "score": 0
            }
        ],
        "robots": [],
        "balls": []
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def setBalls(self,balls):
        self.data["balls"] = balls
        self.setTime(datetime.now())

    def setRobots(self,robots):
        self.data["robots"] = robots
        self.setTime(datetime.now())

    def setTime(self,time):
        self.data["time"] = time

        

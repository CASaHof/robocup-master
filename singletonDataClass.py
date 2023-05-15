from enum import Enum

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

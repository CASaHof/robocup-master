
from typing import List
from src.classes.Ball import Ball
from src.classes.Robot import Robot


class Frame:
    time: int = 0
    robot: List[Robot] = []
    ball: List[Ball] = []

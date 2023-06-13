from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Robot:
    x: int
    y: int
    id: str
    angle: int
    def copy(self):
        r = Robot(self.x,self.y,self.id,self.angle)
        return r
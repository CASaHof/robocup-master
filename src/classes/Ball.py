from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Ball:
    x: int
    y: int
    def copy(self):
        r = Ball(self.x,self.y)
        return r
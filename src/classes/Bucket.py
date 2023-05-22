from dataclasses import dataclass
from src.classes import FrameCouples

from src.classes import Frame

@dataclass
class Bucket:
    client1: Frame = None
    client2: Frame = None
    framecouples: FrameCouples = None
    debug: bool = False

    def __init__(self,framecouples:FrameCouples,debug=False):
        self.framecouples = framecouples
        self.debug = debug
    
    def print(self,text):
        if(self.debug):
            print(text)

    def addFrameClient1(self, frame: Frame):
        self.print("client1")
        self.client1 = frame
        self.checkClientState()

    def addFrameClient2(self, frame: Frame):
        self.print("client2")
        self.client2 = frame
        self.checkClientState()

    def checkClientState(self):
        if(self.client1 != None and self.client2 != None):
            client1 = self.client1
            client2 = self.client2
            return client1,client2
        return None,None

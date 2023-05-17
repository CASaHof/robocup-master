from typing import List
from os.path import exists
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import asyncio
import websockets
import jsonpickle

from dotenv import dotenv_values
from CASTOKEN import CASTOKEN


config = dotenv_values(".env")

from src.web.server import runWebserver

from os.path import exists
import sys

if not exists("./.env"):
    print("[ERROR] .env not found. Did you install?")
    print("https://github.com/redigermany/cas-robocup-master/#install")
    sys.exit()

@dataclass_json
@dataclass
class Ball:
    x: int
    y: int

@dataclass_json
@dataclass
class Robot:
    x: int
    y: int
    id: str
    angle: int

class Frame:
    time: int = 0
    robot: List[Robot] = []
    ball: List[Ball] = []


class FrameCouples:
    _frames = []
    _current = -1

    def __init__(cls,l):
        print(f"Creating new Frames with length {l}")
        for i in range(l):
            cls._frames.append(None)

    def getAll(self):
        return self._frames

    def update(self,data):
        self._current = self._current + 1
        if self._current >= len(self._frames):
            self._current = 0
        self._frames[self._current] = data

framecouples = FrameCouples(10)

@dataclass
class Bucket:
    client1: Frame = None
    client2: Frame = None

    def addFrameClient1(self, frame: Frame):
        print("client1")
        self.client1 = frame
        self.checkClientState()

    def addFrameClient2(self, frame: Frame):
        print("client2")
        self.client2 = frame
        self.checkClientState()

    def checkClientState(self):
        if(self.client1 != None and self.client2 != None):
            print("updated")
            framecouples.update([self.client1,self.client2])
            self.client1 = None
            self.client2 = None

bucket = Bucket()
# class Frame:
#     _next = None
#     _data = {}

#     def __new__(cls,data):
#         cls._data = data
    
#     def hasNext(self):
#         return self._next!=None
    
#     def next(self):
#         return self._next
    
#     def get(self):
#         return self._data


class DataStore(object):
    _instance = None

    data = {
        "clients": {},
        "teamServer": {},
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def setBalls(self,balls):
        self.data["balls"] = balls

    def setRobots(self,robots):
        self.data["robots"] = robots

    def checkClient(self,id):
        return id in self.data["clients"]

    def addClient(self,id,websocket,user):
        if not self.checkClient(id):
            self.data["clients"][id] = {
                "websocket":websocket,
                "user":user
            }
        return self.data["clients"][id]
        
    def removeClient(self,id):
        if self.checkClient(id):
            del self.data["clients"][id]
    
    def getClient(self,id):
        if self.checkClient(id):
            return self.data["clients"][id]["user"]
        return None

ds = DataStore()

async def show_time(websocket):
    while websocket.close_rcvd==None:
        # await websocket.send(jsonpickle.encode({"type":"message","message":"deine Mudda0"})) # Teamserver Datapackage
        message = await websocket.recv()
        json = jsonpickle.decode(message)
        if "type" in json:
            if json["type"]=="auth" and "token" in json:
                if json["token"] in CASTOKEN:
                    user = CASTOKEN[json["token"]]
                    ds.addClient(websocket.id,websocket,user)
                    await websocket.send(jsonpickle.encode({"type":"authenticated","message":f"Welcome {user['UUID']}"},unpicklable=False))
            user = ds.getClient(websocket.id)
            #if json["type"]=="data" and "data" in json and user:
            #    print(f"Message from {user['UUID']}: {json}")
        #print(json)
        if "data" in json:
            user = ds.getClient(websocket.id)
            newFrame = Frame()
            newFrame.robot = []
            newFrame.ball = []
            if "time" in json["data"]:
                newFrame.time = json["data"]["time"]
            if "balls" in json["data"]:
                for idx in json["data"]["balls"]:
                    temp = Ball.from_dict(idx)
                    newFrame.ball.append(temp)
            if "robots" in json["data"]:
                for idx in json["data"]["robots"]:
                    temp = Robot.from_dict(idx)
                    newFrame.robot.append(temp)
            #print(newFrame.robot)
            #print(newFrame.ball)
            if(user["UUID"] == "Client-1"):
                bucket.addFrameClient1(newFrame)
            if(user["UUID"] == "Client-2"):
                bucket.addFrameClient2(newFrame)
            bucket.checkClientState()
        await asyncio.sleep(1/10)
    ds.removeClient(websocket.id)

async def do_start_websocket():
    WS_PORT = int(config.get("WS_PORT"))

    WS_HOST = "localhost"
    if(len(sys.argv)>1):
        WS_HOST = sys.argv[1]

    async with websockets.serve(show_time, WS_HOST, WS_PORT):
        print(f"Websocket listening on ws://{WS_HOST}:{WS_PORT}")
        await asyncio.Future()  # run forever   

def start_websocket():  
    asyncio.run(do_start_websocket())
    
# Start Server
def startServer():
    # http = threading.Thread(target=runWebserver, daemon=True)
    # http.start()
    start_websocket()

if __name__ == "__main__":
    startServer()
import asyncio
import websockets
import jsonpickle
import sys

from src.classes.DataStore import DataStore
from src.classes.FrameCouples import FrameCouples
from src.classes.Frame import Frame
from src.classes.Ball import Ball
from src.classes.Robot import Robot
from src.classes.Bucket import Bucket
from src.CASENV import CASENV
from CASTOKEN import CASTOKEN

from src.web.server import runWebserver

framecouples = FrameCouples(10)

bucket = Bucket(framecouples)
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
    WS_PORT = CASENV.WS_PORT

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
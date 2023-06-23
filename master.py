import asyncio
from datetime import datetime
import threading
import websockets
import jsonpickle
import sys

from src import DataStore, FrameCouples, Frame, Ball, Robot, Bucket,CASENV,runWebserver
from CASTOKEN import CASTOKEN
from src.classes.singletonDataClass import Singleton
from src.lib.normalizePositions import normalizePositions

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
s1 = Singleton()

async def show_time(websocket):
    global bucket
    
    now = datetime.now()
    time = now.second
    fps = 0


    while websocket.close_rcvd==None:
        # await websocket.send(jsonpickle.encode({"type":"message","message":"deine Mudda0"})) # Teamserver Datapackage
        try:
            message = await websocket.recv()
            json = jsonpickle.decode(message)
            if "type" in json:
                if json["type"]=="auth" and "token" in json:
                    if json["token"] in CASTOKEN:
                        user = CASTOKEN[json["token"]]
                        if user.type == "client":
                            ds.addClient(websocket.id,websocket,user)
                        elif user.type=="team":
                            ds.addTeamServer(websocket.id,websocket,user)
                        elif user.type=="web":
                            ds.addWebClient(websocket.id,websocket,user)
                        else:
                            pass
                        await websocket.send(jsonpickle.encode({"type":"authenticated","message":f"Welcome {user.UUID}"},unpicklable=False))
                user = ds.getClient(websocket.id)
                #if json["type"]=="data" and "data" in json and user:
                #    print(f"Message from {user['UUID']}: {json}")
            if json["type"]=="score":
                
                if json["team"]=="up":
                    if json["update"]=="+":
                        s1.data["teams"][0]["score"] += 1
                    if json["update"]=="-":
                        s1.data["teams"][0]["score"] -= 1
                if json["team"]=="down":
                    if json["update"]=="+":
                        s1.data["teams"][1]["score"] += 1
                    if json["update"]=="-":
                        s1.data["teams"][1]["score"] -= 1
                
                # s1.data
                # { "type": "score", "team": "up", "update": "-" }
                # { "type": "score", "team": "up", "update": "+" }
                # { "type": "score", "team": "down", "update": "-" }
                # { "type": "score", "team": "down", "update": "+" }

            if "data" in json:
                user = ds.getClient(websocket.id)
                newFrame = Frame()
                newFrame.robot = []
                newFrame.ball = []
                # print(json["data"])
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
                # print(newFrame.robot)
                # print(user.UUID,newFrame.ball)
                if len(newFrame.robot)>0 or len(newFrame.ball)>0:
                    if(user.UUID == "CameraClient-1"):
                        bucket.addFrameClient1(newFrame)
                    if(user.UUID == "CameraClient-2"):
                        bucket.addFrameClient2(newFrame)
                    client1,client2 = bucket.checkClientState()
                    if(client1 != None or client2 != None ):
                        now = datetime.now()
                        currtime = now.second
                        if currtime != time:
                            print(f"FPS = {fps}")
                            time = currtime
                            fps = 0
                        else:
                            fps = fps + 1 
                        bucket = Bucket(FrameCouples())
                        framecouples.update([client1, client2])
                        # c1, c2 = framecouples.getCurrent()
                        # for robot in client1.robot:
                        # print(client1.robot,client2.robot)
                        normalizedRobots = normalizePositions(client1.robot,client2.robot)
                        normalizedBalls = normalizePositions(client1.ball,client2.ball)
                        # print(t)
                        # TODO: SEND IT
                        message = {
                            "state": "playing",
                            "time_remaining": 1337,
                            "teams": s1.data["teams"],
                            "robots": normalizedRobots,
                            "balls": normalizedBalls,
                            "timestamp": round(datetime.now().timestamp())
                        }
                        clientz = ds.getTeamServerClients()
                        for clt in clientz:
                            # print(clientz[clt])
                            ws = clientz[clt]["websocket"]
                            if ws!=None and ws.close_rcvd==None:
                                await ws.send(jsonpickle.encode({"type":"data","message":message},unpicklable=False))
                            else:
                                del clientz[clt]
                        clientz = ds.getWebClients()
                        try:
                            for clt in clientz:
                                # print(clientz[clt])
                                ws = clientz[clt]["websocket"]
                                if ws!=None and ws.close_rcvd==None:
                                    await ws.send(jsonpickle.encode({"type":"data","message":message},unpicklable=False))
                                else:
                                    del clientz[clt]
                        except:
                            pass
        except:
            pass



        await asyncio.sleep(1/10)
    ds.removeClient(websocket.id)

async def do_start_websocket():
    WS_PORT = CASENV.WS_PORT

    WS_HOST = "192.168.171.136"
    if(len(sys.argv)>1):
        WS_HOST = sys.argv[1]

    async with websockets.serve(show_time, WS_HOST, WS_PORT):
        print(f"Websocket listening on ws://{WS_HOST}:{WS_PORT}")
        await asyncio.Future()  # run forever   

def start_websocket():  
    asyncio.run(do_start_websocket())
    
# Start Server
def startServer():
    http = threading.Thread(target=runWebserver, daemon=True)
    http.start()
    start_websocket()

if __name__ == "__main__":
    startServer()
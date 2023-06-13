import asyncio
import jsonpickle
import websockets
import sys
from src import Singleton,CASENV

WS_PORT = CASENV.WS_PORT
WS_AUTH = CASENV.WS_AUTH

WS_HOST = "localhost"
if(len(sys.argv)>1):
    WS_HOST = sys.argv[1]

uri = f"ws://{WS_HOST}:{WS_PORT}"

authed = False

print(f"Connecting to {uri}")

async def establishConnection():
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                with open("data.log", "a") as myfile:
                    print(f"Connected to {uri}")
                    await websocket.send(jsonpickle.encode({"type":"auth","token":"geg#sqIDA0HKwRygxPNpU"},unpicklable=False))
                    # print(jsonpickle.encode(websocket,unpicklable=False))
                    while websocket.close_rcvd==None:
                        message = await websocket.recv()
                        json = jsonpickle.decode(message)
                        print(json)
                        myfile.write(message+"\n")

        except:
            pass
if __name__ == "__main__":
    asyncio.run(establishConnection())
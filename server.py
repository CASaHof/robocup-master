import asyncio
import random
import websockets
import jsonpickle
import threading
import datetime

from src.web.server import runWebserver

async def show_time(websocket):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(jsonpickle.encode({
            "state": "debug",
            "time_remaining": message,
            "robots": [
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "blue",
                    "angle": random.random()*360,
                },
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "green",
                    "angle": random.random()*360,
                },
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "yellow",
                    "angle": random.random()*360,
                },
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "pink",
                    "angle": random.random()*360,
                }
            ],
            "balls": [
                {
                    "x": random.random(),
                    "y": random.random(),
                }   
            ]
        }))
        await asyncio.sleep(1)

async def do_start_websocket():
    async with websockets.serve(show_time, "localhost", 8765):
        await asyncio.Future()  # run forever

def start_websocket():
    asyncio.run(do_start_websocket())
    
# Start Server
def main():
    http = threading.Thread(target=runWebserver, daemon=True)
    http.start()
    start_websocket()

if __name__ == "__main__":
    main()

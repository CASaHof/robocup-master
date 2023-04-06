import asyncio
import websockets
import jsonpickle
import threading
import datetime

from src.web.server import runWebserver

async def show_time(websocket):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(jsonpickle.encode({"time":message}))
        await asyncio.sleep(1/30)

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

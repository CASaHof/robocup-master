from datetime import datetime
import random
import threading
from ultralytics import YOLO
from yt_dlp import YoutubeDL
from os.path import exists
import time
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

import asyncio
import websockets
import jsonpickle
import threading

from enum import Enum

from dotenv import dotenv_values
config = dotenv_values(".env")

from src.web.server import runWebserver

from os.path import exists
import sys

if not exists("./.env"):
    print("[ERROR] .env not found. Did you install?")
    print("https://github.com/redigermany/cas-robocup-master/#install")
    sys.exit()



async def show_time(websocket):
    while websocket.close_rcvd!=None:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        #await websocket.send(jsonpickle.encode(s1.data))
        await websocket.send("deine Mudda0") # Teamserver Datapackage
        await asyncio.sleep(1/10)

async def do_start_websocket():
    WS_PORT = int(config.get("WS_PORT"))
    async with websockets.serve(show_time, "localhost", WS_PORT):
        print(f"Websocket listening on ws://localhost:{WS_PORT}")
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
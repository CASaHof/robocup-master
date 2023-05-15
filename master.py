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
from CASTOKEN import CASTOKEN


config = dotenv_values(".env")

from src.web.server import runWebserver

from os.path import exists
import sys

if not exists("./.env"):
    print("[ERROR] .env not found. Did you install?")
    print("https://github.com/redigermany/cas-robocup-master/#install")
    sys.exit()

class Frames:
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

class Frame:
    _next = None
    _data = {}

    def __new__(cls,data):
        cls._data = data
    
    def hasNext(self):
        return self._next!=None
    
    def next(self):
        return self._next
    
    def get(self):
        return self._data


class DataStore(object):
    _instance = None

    data = {
        "clients": {},
        "teamServer": {},
        "frames": Frames(10)
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

    def makeClientSure(self,id,websocket):
        if not self.checkClient(id):
            self.data["clients"][id] = websocket
        return self.data["clients"][id]
        
    def removeClient(self,id):
        if self.checkClient(id):
            del self.data["clients"][id]

ds = DataStore()

async def show_time(websocket):
    while websocket.close_rcvd==None:
        client = ds.makeClientSure(websocket.id,websocket)
        # message = datetime.datetime.utcnow().isoformat() + "Z"
        #await websocket.send(jsonpickle.encode(s1.data))
        await websocket.send(jsonpickle.encode({"type":"message","message":"deine Mudda0"})) # Teamserver Datapackage
        message = await websocket.recv()
        json = jsonpickle.decode(message)
        if "type" in json:
            if json["type"]=="auth" and "token" in json:
                if json["token"] in CASTOKEN:
                    await websocket.send(jsonpickle.encode({"type":"authenticated"},unpicklable=False))
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
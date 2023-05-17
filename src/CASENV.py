from dotenv import dotenv_values
from os.path import exists
import sys

config = dotenv_values(".env")

if not exists("./.env"):
    print("[ERROR] .env not found. Did you install?")
    print("https://github.com/redigermany/cas-robocup-master/#install")
    sys.exit()

def getStr(name:str,default:str):
    temp = config.get(name)
    if temp==None:
        print(f"[WARNING] Missing {name} in .env")
        if default!=None:
            print(f"          Using default value {default}")
            print(f"          Consider adding {name}={default}\n")
            temp = default
        else:
            print(f"          No Default value given. Exiting.")
            sys.exit()
    return str(temp)
    
def getInt(name:str,default:int):
    temp = config.get(name)
    if temp==None:
        print(f"[WARNING] Missing {name} in .env")
        if default!=None:
            print(f"          Using default value {default}")
            print(f"          Consider adding {name}={default}\n")
            temp = default
        else:
            print(f"          No Default value given. Exiting.")
            sys.exit()
    return int(temp)

class CASENV:
    WS_PORT = getInt("WS_PORT",8765)
    WEB_PORT = getInt("WEB_PORT",8764)
    WS_AUTH = getStr("WS_AUTH",None)
    CAM_ID = getInt("CAM_ID",None)
    VIDEO_WIDTH = getInt("VIDEO_WIDTH",640)
    VIDEO_HEIGHT = getInt("VIDEO_HEIGHT",480)


# if __name__=="__main__":
    # print(CASENV)
from dotenv import dotenv_values
from os.path import exists
import sys

config = dotenv_values(".env")

if not exists("./.env"):
    print("[ERROR] .env not found. Did you install?")
    print("https://github.com/redigermany/cas-robocup-master/#install")
    sys.exit()

class CASENV:
    WS_PORT = int(config.get("WS_PORT"))
    WEB_PORT = int(config.get("WEB_PORT"))
    WS_AUTH = str(config.get("WS_AUTH"))
    CAM_ID = int(config.get("CAM_ID"))

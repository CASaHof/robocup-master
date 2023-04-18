from ultralytics import YOLO
from yt_dlp import YoutubeDL
from os.path import exists


model = YOLO('./best.pt')  # load an official detection model
youtube_id = "4_BWQl91p9Y"
if "youtube_id" in locals() and youtube_id!="":
    file_exists = exists("./"+youtube_id+".mp4")
    if not file_exists:
        print(f"Downloading {youtube_id}")
        ydl_opts = {
            "outtmpl": youtube_id+".mp4"
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v='+youtube_id])
    else:
        print(f"{youtube_id} already existing.")
else:
    print("No youtube_id given!")

results = model(source=f"{youtube_id}.mp4", show=True, stream=True) 
for result in results:
   boxes = result.boxes  # Boxes object for bbox outputs
   for idx,c in enumerate(result.boxes.cls):
    if result.names[int(c)]=="robot":
        print(f"c={c} ({result.names[int(c)]}) {boxes.xyxy[idx]}")
#    result={0: 'ball', 1: 'centercircle', 2: 'goal', 3: 'line', 4: 'penaltycross', 5: 'robot'}
#    print(f"result={result.names}")
#    print(f"boxes={boxes.xyxy[0]}")


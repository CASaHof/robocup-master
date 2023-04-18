from ultralytics import YOLO

# https://docs.ultralytics.com/modes/predict/?h=boxes#boxes

model = YOLO('../best.pt')  # load an official detection model
results = model(source="https://www.youtube.com/watch?v=4_BWQl91p9Y", show=True, stream=True) 
for result in results:
   boxes = result.boxes  # Boxes object for bbox outputs
   for idx,c in enumerate(result.boxes.cls):
    if result.names[int(c)]=="robot":
        print(f"c={c} ({result.names[int(c)]}) {boxes.xyxy[idx]}")
#    result={0: 'ball', 1: 'centercircle', 2: 'goal', 3: 'line', 4: 'penaltycross', 5: 'robot'}
#    print(f"result={result.names}")
#    print(f"boxes={boxes.xyxy[0]}")

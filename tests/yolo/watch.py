from ultralytics import YOLO

# https://docs.ultralytics.com/modes/predict/?h=boxes#boxes

model = YOLO('../best.pt')  # load an official detection model
# results = model(source="https://www.youtube.com/watch?v=RlAhM2lu1XE", show=True) 
results = model(source="https://www.youtube.com/watch?v=ggSlL_ddYQc", show=True) 

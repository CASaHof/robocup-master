from ultralytics import YOLO

# Load a model
# model = YOLO("yolov8s-seg.pt")  # load a pretrained model 
model = YOLO("yolov8x-seg.pt")  # load a pretrained model 

# Train the model
results = model.train(data="data.yaml", imgsz=640, batch=8, epochs=500, plots=True, cache=True)

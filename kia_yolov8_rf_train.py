from ultralytics import YOLO
from IPython.display import display, Image

display.clear_output()
ultralytics.checks()

# Load a model
model = YOLO("weights/yolov8n.pt")
results = model.train(data="Kitchen-Intelligent-Assistant-2\data.yaml", imgsz=640, batch=8, epochs=20, plots=False)
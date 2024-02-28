from roboflow import Roboflow

rf = Roboflow(api_key="7gqyul75jvef76MNUFCI")
project = rf.workspace("kia-qemlp").project("kitchen-intelligent-assistant")
dataset = project.version(2).download("yolov8")
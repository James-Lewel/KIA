import cv2
import numpy as np
import threading
import torch
import torchvision.transforms.functional as F

# Choose the MiDaS model type
# model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
# model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

# Load the selected MiDaS model
midas = torch.hub.load("intel-isl/MiDaS", model_type, pretrained=True, trust_repo=True)
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

# Load MiDaS transforms
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

@torch.no_grad()
def process(image, batch):
    prediction = midas(batch)
    prediction = (
        torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=(image.shape[0], image.shape[1]),
            mode="bicubic",
            align_corners=False,
        )
        .squeeze()
        .cpu()
        .numpy()
    )
    prediction = (prediction - prediction.min()) / (prediction.max() - prediction.min())
    
    return prediction

# Class to handle depth camera operations
class Midas_Depth:
    def __init__(self, camera_instance = None):
        self.camera = camera_instance
        self.depth_image = None
        self.is_running = True
        pass
            
    # Method to get the processed depth image
    def get_depth_image(self, frame):
        #frame = self.camera.get_image()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        batch = transform(image).to('cpu')
        self.depth_image = process(image, batch)
        return self.depth_image if self.depth_image is not None else np.zeros((240, 320, 3), dtype=np.uint8)
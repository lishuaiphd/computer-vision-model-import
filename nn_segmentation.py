import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np

MODEL_PATH = 'models/segmentation.pth'

class SimpleSegModel:
    def __init__(self, device='cpu'):
        self.device = device
        self.model = None

    def predict_mask(self, pil_img: Image.Image) -> np.ndarray:
        w,h = pil_img.size
        return np.zeros((h,w), dtype=np.uint8)

if __name__ == '__main__':
    print('Neural segmentation scaffold. Add your model and inference logic here.')
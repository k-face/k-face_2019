from PIL import Image
import numpy as np
import cv2
from torchvision import transforms as trans
from config import configuration

MEAN = [0.5, 0.5, 0.5]
STD = [0.5, 0.5, 0.5]
TARGET_IMAGE_SIZE = configuration().inputSize

def image_norm(fname):
    img = Image.open(fname, 'r')
    if img.size[0] == 0 | img.size[1] == 0:
        return 0

    resize_img = img.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE))

    if len(resize_img.split()) == 1:
        gray_img = np.asarray(((np.float32(resize_img) / 255.0)-MEAN[0])/STD[0])
    elif len(resize_img.split()) == 3:
        resize_img = resize_img.convert('L')
        gray_img = np.asarray(((np.float32(resize_img) / 255.0)-MEAN[0])/STD[0])
    else:
        return 0
    normImg = np.asarray([gray_img])

    return normImg



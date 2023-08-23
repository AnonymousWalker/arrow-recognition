
import cv2
import numpy as np
from src.image_processor import detect_directions_from_img

img = cv2.imread('resources/bug/b2.png')

result = detect_directions_from_img(img)
print(result)
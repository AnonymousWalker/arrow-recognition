
import cv2
import numpy as np
from src.image_processor import detect_directions_from_img, output_class

img = cv2.imread('resources/bug/5.png')

result = detect_directions_from_img(img)
print(result)


def count_blue_pixels(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds for detecting blue color
    lower_blue = np.array([90, 50, 50])  # Adjust these values as needed
    upper_blue = np.array([130, 255, 255])  # Adjust these values as needed
    
    # Create a mask to isolate blue pixels
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    
    # Count the number of blue pixels
    blue_pixel_count = np.sum(blue_mask > 0)
    
    return blue_pixel_count

# img = cv2.imread('out/white.png')
# print(count_blue_pixels(img))
# img = cv2.imread('out/bg2.png')
# print(count_blue_pixels(img))
import cv2
import numpy as np
import mss
import time
from PIL import Image, ImageEnhance

def is_red(image):
    # Split the image into color channels
    blue_channel, green_channel, red_channel = cv2.split(image)
    
    # Calculate the average intensities of red and blue channels
    average_red_intensity = np.mean(red_channel)
    average_blue_intensity = np.mean(blue_channel)
    
    # Compare average intensities to determine if the image is more red than blue
    if average_red_intensity > average_blue_intensity:
        return True
    else:
        return False    
    

def is_more_red_than_white(image):    
    # Calculate the average intensity of the red channel
    red_channel = image[:, :, 2]  # Red channel is at index 2
    average_red_intensity = np.mean(red_channel)
    
    # Calculate the average intensity of all color channels (white)
    white_intensity = np.mean(image)
    
    # Compare average red intensity to average white intensity
    if average_red_intensity > white_intensity:
        return True
    else:
        return False
    
def count_red_pixels(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds for detecting red color
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    
    # Create a mask to isolate red pixels
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    
    # Count the number of red pixels
    red_pixel_count = np.sum(red_mask > 0)
    
    return red_pixel_count

def count_gray_pixels(image):
    gray_pixels = 0
    height, width, _ = image.shape
    tolerance = 10
    
    for y in range(height):
        for x in range(width):
            b, g, r = image[y, x]
            if abs(r - g) <= tolerance and abs(g - b) <= tolerance:
                gray_pixels += 1
                
    return gray_pixels

def capture_screenshot_with_time(window, area):
    window_rect = window.rectangle()
    screenshot_area = {
        "left": window_rect.left + area[0],
        "top": window_rect.top + area[1],
        "width": area[2],
        "height": area[3],
    }
    with mss.mss() as sct:
        timestamp = time.time()
        screenshot = sct.grab(screenshot_area)
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
        
        return screenshot_bgr, timestamp
    

def adjust_contrast_brightness(cv2_image, contrast_factor, brightness_factor):
    """ example: (image, contrast_factor=1.5, brightness_factor=1.2) """

    image = Image.fromarray(cv2_image)

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)
    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)
    
    adjusted_image_cv2 = np.array(image)

    return adjusted_image_cv2
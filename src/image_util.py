import cv2
import numpy as np

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
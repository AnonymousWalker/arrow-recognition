import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
import logging
from tensorflow.keras.models import load_model
import imutils
from src.image_util import is_red, count_gray_pixels
import src.image_util as image_util

output_class = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right', 'unknown']
output_class_reversed = ['down', 'up', 'right', 'left', 'down-right', 'down-left', 'up-right', 'up-left', 'unknown']

template = cv2.imread('resources/head.png')
model = load_model('trained-model/v2.0-gray.h5')

def predict_direction2(input_cv2_image):
    target_size = (28, 28)  # Make sure it matches the size your model expects

    input_image_converted = cv2.cvtColor(input_cv2_image, cv2.COLOR_RGB2GRAY)

    # Resize and preprocess the image
    pil_image = Image.fromarray(input_image_converted)
    image = pil_image.resize(target_size)
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(image, verbose=None)

    # if np.max(predictions) < 0.7:
    #     return len(output_class) - 1    # 'unknown'

    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class

    return predicted_class

def detect_directions_from_img(image):
    enhanced_image = image_util.adjust_contrast_brightness(image, contrast_factor=1.3, brightness_factor=1.15)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(enhanced_image, cv2.COLOR_RGB2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply binary thresholding to create a binary image
    _, threshold_image = cv2.threshold(blurred_image, 130, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    cnts = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Sort contours by x-coordinate
    cnts = sorted(cnts, key=lambda c: cv2.boundingRect(c)[0])

    directions = []

    for contour in cnts:
        # Extract the region corresponding to the contour
        x, y, w, h = cv2.boundingRect(contour)

        # filter square regions resembling arrow key
        if abs(w - h) > 15 or h < 20 or w < 20:
            continue

        contour_region = enhanced_image[y:y+h, x:x+w]
        if count_gray_pixels(contour_region) >= 700: # gray-color arrow
            continue
        
        predicted_class_id = predict_direction2(contour_region)

        # determine if the direction is reversed (red key)
        predicted_result = output_class_reversed[predicted_class_id] if is_red(contour_region) else output_class[predicted_class_id]
            
        if predicted_result != 'unknown':
            directions.append(predicted_result)
    
    return directions

def get_head_position(template_image, main_image):
    # Finds the position of the playback head

    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    template_height, template_width = template_image.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    center_x = (top_left[0] + bottom_right[0]) // 2
    center_y = (top_left[1] + bottom_right[1]) // 2

    return (center_x, center_y)
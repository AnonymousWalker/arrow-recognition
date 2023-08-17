import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import imutils
from src.image_util import is_red

output_class = ['down', 'left', 'right', 'up']
output_class_reversed = ['up', 'right', 'left', 'down'] # reversed list of output_class
template = cv2.imread('resources/head.png')
model = load_model('trained-model/model_v1.h5')

def predict_direction2(input_cv2_image):
    # Preprocess the input image from cv2.imread
    target_size = (28, 28)  # Make sure it matches the size your model expects

    # Convert BGR image to RGB (since PIL uses RGB)
    input_image_rgb = cv2.cvtColor(input_cv2_image, cv2.COLOR_BGR2RGB)

    # Resize and preprocess the image
    pil_image = Image.fromarray(input_image_rgb)
    image = pil_image.resize(target_size)
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(image, verbose=0)

    # Interpret the predictions
    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class
    # Here, you might need a class mapping to convert index to class label

    return predicted_class

def detect_directions_from_img(image):

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply binary thresholding to create a binary image
    _, threshold_image = cv2.threshold(blurred_image, 100, 255, cv2.THRESH_BINARY)

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

        contour_region = image[y:y+h, x:x+w]
        predicted_class_id = predict_direction2(contour_region)

        # determine if the direction is reversed (red key)
        predicted_result = output_class_reversed[predicted_class_id] if is_red(contour_region) else output_class[predicted_class_id]
            
        directions.append(predicted_result)
    
    return directions

def get_head_position(template_image, main_image):
    # Finds the position of the playback head

    # Perform template matching
    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    template_height, template_width = template_image.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    center_x = (top_left[0] + bottom_right[0]) // 2
    center_y = (top_left[1] + bottom_right[1]) // 2

    return (center_x, center_y)
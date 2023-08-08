import cv2
import imutils
import numpy as np
from tensorflow.keras.models import load_model

output_class = ['down', 'left', 'right', 'up']

def detect_directions_from_img(image_path, model):
    # Read the image from the file
    image = cv2.imread(image_path)

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
        region = image[y:y+h, x:x+w]

        # Preprocess the region for prediction
        resized_region = cv2.resize(region, (28, 28))
        resized_region = resized_region / 255.0  # Normalize pixel values
        resized_region = resized_region[np.newaxis, :, :, :]

        # Predict using the model
        predictions = model.predict(resized_region)
        predicted_class = np.argmax(predictions)

        directions.append(output_class[predicted_class])
    
    return directions

# Load the trained model
model = load_model('trained-model/arrow_orientation_model.h5')

# Call the function with the input image path - this image is the cropped KEYS AREA
dirs = detect_directions_from_img('resources/s1-crop.png', model)
print(dirs)
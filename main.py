import cv2
import imutils
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

output_class = ['down', 'left', 'right', 'up']

# Load the trained model
model = load_model('trained-model/arrow_orientation_model.h5')

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
    predictions = model.predict(image)

    # Interpret the predictions
    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class
    # Here, you might need a class mapping to convert index to class label

    return output_class[predicted_class]



def detect_directions_from_img(image_path):
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

        # filter square regions resembling arrow key
        if abs(w - h) > 10 or h < 30 or w < 30:
            continue

        contour_region = image[y:y+h, x:x+w]
        predicted_class = predict_direction2(contour_region)

        directions.append(predicted_class)
    
    return directions


# Call the function with the input image path - this image is the cropped KEYS AREA
dirs = detect_directions_from_img('resources/arrows2.png')
print(dirs)
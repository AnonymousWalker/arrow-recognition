import cv2
import imutils
import numpy as np
import mss
import pywinauto
import keyboard
from PIL import Image
from tensorflow.keras.models import load_model

output_class = ['down', 'left', 'right', 'up']
model = load_model('trained-model/arrow_orientation_model.h5')

# Load the trained model

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



def detect_directions_from_img(image):
    # Read the image from the file
    # image = cv2.imread(image_path)

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
# dirs = detect_directions_from_img('resources/arrows2.png')
# print(dirs)


# area: (left, top, width, height)
def capture_screenshot_with_app(pid, area):
    app = pywinauto.Application().connect(process=pid)
    # window = app.window()  # Get the main window of the application
    window = app["Audition"]
    window.set_focus()
    window_rect = window.rectangle()
    screenshot_area = {
        "left": window_rect.left + area[0],
        "top": window_rect.top + area[1],
        "width": area[2],
        "height": area[3],
    }
    with mss.mss() as sct:
        screenshot = sct.grab(screenshot_area)
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGBA2RGB)
        
        return screenshot_bgr


def trigger_screenshot():    
    process_id = 21672
    area = (280, 540, 470, 40) # (left, top, width, height)

    # Capture a screenshot of the application window and save it
    captured_image = capture_screenshot_with_app(process_id, area)

    # Call the function to detect directions from the captured image
    dirs = detect_directions_from_img(captured_image)
    print(dirs)

    cv2.imwrite('out/captured.png', captured_image)


# Register the trigger function to the desired key press event
def key_listener(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'enter':
        trigger_screenshot()
        

keyboard.hook(callback=key_listener)
# Keep the script running
keyboard.wait('esc')  # Wait for the 'esc' key to exit

# Unregister the trigger function
keyboard.unhook_all()


# process_id = 10800
# area = (280, 540, 470, 40) # (left, top, width, height)
# captured_img = capture_screenshot_with_app(process_id, area)


# image = cv2.imread('out/captured.png')
# d = detect_directions_from_img(image)
# print(d)
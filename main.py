import cv2
import time
import imutils
import numpy as np
import mss
import pywinauto
from pywinauto import keyboard as pwkeyboard
import keyboard
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from src.keyboard_ctrl import KeyDef, KeyboardCtrl
from src.key_color import KeyColor

tf.get_logger().setLevel('ERROR')

KEY_TYPING_SLEEP = 0.00001
output_class = ['down', 'left', 'right', 'up']
output_class_reversed = ['up', 'right', 'left', 'down'] # reversed list of output_class
class_to_key = { 
    'up': KeyDef.VK_UP, 
    'down': KeyDef.VK_DOWN, 
    'left': KeyDef.VK_LEFT, 
    'right': KeyDef.VK_RIGHT
}
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
    predictions = model.predict(image, verbose=0)

    # Interpret the predictions
    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class
    # Here, you might need a class mapping to convert index to class label

    return predicted_class


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


# area: (left, top, width, height)
def capture_screenshot_app_window(window, area):
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


def trigger_screenshot(window):    
    area = (280, 540, 470, 40) # (left, top, width, height)

    # Capture a screenshot of the application window and save it
    captured_image = capture_screenshot_app_window(window, area)

    # Call the function to detect directions from the captured image
    dirs = detect_directions_from_img(captured_image)

    send_key_input(window, dirs)

    # cv2.imwrite('out/captured{0}.png'.format(time.time()), captured_image)


def send_key_input(window, arrows):
    window.set_focus()
    print(arrows)
    for arr in arrows:
        key = class_to_key[arr]

        KeyboardCtrl.press_and_release(key)
        time.sleep(KEY_TYPING_SLEEP)


# Register the trigger function to the desired key press event
def key_listener(e, window):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'enter':
        trigger_screenshot(window)
        

# main
pid = 18320
app = pywinauto.Application().connect(process=pid)
window = app["Audition"]
keyboard.hook(callback=lambda e: key_listener(e, window))
keyboard.wait('esc')  # Wait for the 'esc' key to exit
keyboard.unhook_all()


# process_id = 10800
# area = (280, 540, 470, 40) # (left, top, width, height)
# captured_img = capture_screenshot_with_app(process_id, area)


# image = cv2.imread('resources/rev1.png')
# d = detect_directions_from_img(image)
# print(d)
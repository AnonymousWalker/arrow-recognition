import cv2
import time
import numpy as np
import mss
import pywinauto
from pywinauto import keyboard as pwkeyboard
import keyboard
import tensorflow as tf
from src.keyboard_ctrl import KeyDef, KeyboardCtrl
from src.key_color import KeyColor
from src.image_util import *
from src.image_processor import detect_directions_from_img
import threading


tf.get_logger().setLevel('ERROR')

KEY_TYPING_SLEEP = 0.0005
class_to_key = { 
    'up': KeyDef.VK_UP, 
    'down': KeyDef.VK_DOWN, 
    'left': KeyDef.VK_LEFT, 
    'right': KeyDef.VK_RIGHT
}

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
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'enter':
            trigger_screenshot(window)
        # if e.name == 'p': # capture screenshot
        #     captured = capture_screenshot_app_window(window, area=(515,515,170,15))
        #     cv2.imwrite('out/captured{0}.png'.format(time.time()), captured)
        if e.name == 'page up':
            None # increase delay
        if e.name == 'page down':
            None # reduce delay
        
# press perfect when it's time
def watch_perfect(window, perfect_area):
    while True:
        captured = capture_screenshot_app_window(window, perfect_area)
        time.sleep(0.1) 
        if is_more_red_than_white(captured):
            KeyboardCtrl.press_and_release(KeyDef.VK_SPACE)
            time.sleep(0.5)
            trigger_screenshot(window)

# main
pid = 17088
app = pywinauto.Application().connect(process=pid)
window = app["Audition"]

perfect_area = (634, 518, 10, 10)
perfect_thread = threading.Thread(target=lambda: watch_perfect(window, perfect_area))
perfect_thread.daemon = True  # Set the thread as a daemon so it exits when the main thread exits
perfect_thread.start()

keyboard.hook(callback=lambda e: key_listener(e, window))
keyboard.wait('esc')  # Wait for the 'esc' key to exit
keyboard.unhook_all()


# process_id = 10800
# area = (280, 540, 470, 40) # (left, top, width, height)
# captured_img = capture_screenshot_with_app(process_id, area)


# image = cv2.imread('resources/rev1.png')
# d = detect_directions_from_img(image)
# print(d)



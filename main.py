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
from src.image_processor import detect_directions_from_img, get_head_position
from src.speed import speed_map
import threading
import statistics


tf.get_logger().setLevel('ERROR')

KEY_TYPING_SLEEP = 0.001
PERFECT_POS_X = 121.0
ADJUST_SPEED_AMOUNT = 0.1
speed = speed_map[103]

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

def process_arrows(window):    
    area = (280, 540, 470, 40) # (left, top, width, height)

    # Capture a screenshot of the application window and save it
    captured_image = capture_screenshot_app_window(window, area)

    # Call the function to detect directions from the captured image
    dirs = detect_directions_from_img(captured_image)

    send_key_input(window, dirs)

    # cv2.imwrite('out/captured{0}.png'.format(time.time()), captured_image)


def send_key_input(window, arrows):
    window.set_focus()
    time.sleep(KEY_TYPING_SLEEP)
    print(arrows)
    for arr in arrows:
        key = class_to_key[arr]

        KeyboardCtrl.press_and_release(key)


# Register the trigger function to the desired key press event
def key_listener(e, window):
    global speed

    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'enter':
            process_arrows(window)
        if e.name == 'p': # capture screenshot
            captured = capture_screenshot_app_window(window, area=(520,515,8,15))
            cv2.imwrite('out/captured{0}.png'.format(time.time()), captured)
        if e.name == 'page up':
            speed += ADJUST_SPEED_AMOUNT
            print('------ speed: {}'.format(speed))
        if e.name == 'page down':
            speed -= ADJUST_SPEED_AMOUNT
            print('------ speed: {}'.format(speed))
        
def compute_speed(window, head_img, track_area):
    speeds = []
    for i in range(0,8):
            
        track_at_t1, t1 = capture_screenshot_with_time(window, track_area)
        time.sleep(0.5)
        track_at_t2, t2 = capture_screenshot_with_time(window, track_area)

        pos1, _ = get_head_position(head_img, track_at_t1)
        pos2, _ = get_head_position(head_img, track_at_t2)

        if (pos2 < pos1): 
            continue

        s = (pos2 - pos1) * 2
        speeds.append(s)
        
    return statistics.mean(speeds)


# press perfect when it's time
def watch_head(window, head_img, beginning_area, track_area):
    # fps_sleep = 1.0/60

    while True:
        captured = capture_screenshot_app_window(window, beginning_area)
        if count_red_pixels(captured) >= 3: # number of red pixels required to make it recognize the head image
            break
        # else:
        #     time.sleep(fps_sleep)

    current_track, t = capture_screenshot_with_time(window, track_area)
    head_X, _ = get_head_position(head_img, current_track)

    try:
        remaining_time = (PERFECT_POS_X - head_X) / speed # distance / speed
        time.sleep(remaining_time)
        KeyboardCtrl.press_and_release(KeyDef.VK_CONTROL)
        time.sleep(KEY_TYPING_SLEEP)
        print("Ctrl hit!")
    except ValueError:
        # print("value error for sleep()")
        None


def track_thread(window, beginning_area, track_area):
    head_img = cv2.imread('resources/head.png')
    print('speed: {0}'.format(speed))

    while True:
        window.set_focus()
        watch_head(window, head_img, beginning_area, track_area)

# main
pid = 15168
app = pywinauto.Application().connect(process=pid)
window = app["Audition"]

track_area = (515, 515, 170, 15)
beginning_area = (520,515,8,15)
perfect_thread = threading.Thread(target=lambda: track_thread(window, beginning_area, track_area))
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



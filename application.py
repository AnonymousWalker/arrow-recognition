import sys
import cv2
import time
import numpy as np
import mss
import pywinauto
from pywinauto import keyboard as pwkeyboard
import keyboard
from src.keyboard_ctrl import KeyDef, KeyboardCtrl
from src.key_color import KeyColor
from src.image_util import *
from src.image_processor import detect_directions_from_img, get_head_position
from src.speed import bpm_speed_map
import src.util as util
from src.config import Config
import threading
import statistics

class AutoApp:
    def __init__(self, config: Config):
        self.head_img = cv2.imread('resources/head.png')
        self.config = config
        self.config.speed = bpm_speed_map[120]
        self.debug_img = None
        self.debug_arrows = None
        self._focus = True
        self._lock = threading.Lock()

    def capture_screenshot_app_window(self, window, area):
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
            
    def process_arrows(self, window, lock=None):
        # arrow_area = (280, 540, 470, 40) # (left, top, width, height)
        captured_image = self.capture_screenshot_app_window(window, self.config.ARROW_REGION)
        self.debug_img = captured_image
        # debug_img = capture_screenshot_app_window(window, debug_area)

        dirs = detect_directions_from_img(captured_image)

        self.send_key_input(window, dirs)

    def send_key_input(self, window, arrows):
        window.set_focus()
        keys_typed = ""
        print(arrows)
            
        for arr in arrows:
            key = util.class_to_key_code[arr]
            keys_typed += f"{arr}__"

            KeyboardCtrl.press_and_release(key)
            time.sleep(self.config.KEY_TYPING_SLEEP)
        
        self.debug_arrows = keys_typed

    def key_listener(self, e, window):
        if e.event_type == keyboard.KEY_DOWN:
            if e.name == 'pause':
                self.process_arrows(window)
            if e.name == 'f12': # capture screenshot
                print('capturing screenshot...')
                cv2.imwrite('out/{0}__{1}.png'.format(self.debug_arrows, time.time()), self.debug_img)
            

    def watch_to_hit_perfect(self, window, head_img, track_area):
        current_track, t = capture_screenshot_with_time(window, track_area)
        head_X, _ = get_head_position(head_img, current_track)

        try:
            remaining_time = (self.config.PERFECT_POS_X - head_X) / self.config.speed # distance / speed
            time.sleep(remaining_time) # waits until perfect
            KeyboardCtrl.press_and_release(KeyDef.VK_CONTROL)
            print("Ctrl hit!")
        except ValueError:
            None

    def arrows_thread(self, window, track_area):
        lock = threading.Lock()
        while True:
            if not self.get_focus():
                time.sleep(1)
                continue

            self.wait_keys_appear(window, track_area)
            with (lock):
                self.process_arrows(window)

    def start_perfect_watcher(self, window, beginning_area, track_area):
        while True:
            if not self.get_focus():
                time.sleep(1)
                continue

            captured = self.capture_screenshot_app_window(window, beginning_area)
            if count_red_pixels(captured) >= 3:
                # head is at the beginning
                # perfect_thread(window, track_area)
                time.sleep(0.03)
                self.watch_to_hit_perfect(window, self.head_img, track_area)

    def wait_keys_appear(self, window, track_area):
        while True:
            track, _ = capture_screenshot_with_time(window, track_area)
            headX, _ = get_head_position(self.head_img, track)

            if headX >= self.config.PERFECT_POS_X:
                if self.config.CURRENT_LEVEL < 6:
                    time_to_process = self.config.PIXELS_TO_PROCESS / self.config.speed # for low level (1-5)
                    time.sleep(time_to_process)
                elif self.config.speed < 97:
                    time_to_process = self.config.PIXELS_TO_PROCESS / self.config.speed / 2
                    time.sleep(time_to_process)
                elif self.config.speed < 110:
                    time.sleep(0.01)
                
                break
            
    def set_focus(self, isFocused):
        with self._lock:
            self._focus = isFocused

    def get_focus(self):
        with self._lock:
            return self._focus


    def run(self):
        pid = util.get_pid_by_name("Audition.exe")
        app = pywinauto.Application().connect(process=pid)
        window = app["Audition"]
        time.sleep(2)
        print('original speed: {0}'.format(self.config.speed))

        track_area = (515, 515, 170, 15)
        beginning_area = (520, 515, 8, 15)
        per_thread = threading.Thread(target=lambda: self.start_perfect_watcher(window, beginning_area, track_area))
        per_thread.daemon = True  # Set the thread as a daemon so it exits when the main thread exits
        per_thread.start()

        arr_thread = threading.Thread(target=lambda: self.arrows_thread(window, track_area))
        arr_thread.daemon = True
        arr_thread.start()

        keyboard.hook(callback=lambda e: self.key_listener(e, window))
        # keyboard.wait('`')  # Wait for the 'esc' key to exit
        # keyboard.unhook_all()

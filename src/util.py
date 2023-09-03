import psutil
from src.keyboard_ctrl import KeyDef

# initial values
KEY_TYPING_SLEEP = 0.04
PERFECT_POS_X = 120.0
ADJUST_SPEED_AMOUNT = 0.25

class_to_key_code = { 
    'up': KeyDef.VK_UP, 
    'down': KeyDef.VK_DOWN, 
    'left': KeyDef.VK_LEFT, 
    'right': KeyDef.VK_RIGHT,
    'up-left': KeyDef.VK_NUMPAD7,
    'up-right': KeyDef.VK_NUMPAD9,
    'down-left': KeyDef.VK_NUMPAD1,
    'down-right': KeyDef.VK_NUMPAD3,
    'unknown': KeyDef.VK_END
}


def get_pid_by_name(process_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    raise Exception("Audition is not running!")

def log_press_speed(speed):
    if speed == 0.0:
        print("TYPING SPEED LEVEL: 5")
    if speed == 0.01:
        print("TYPING SPEED LEVEL: 4")
    if speed == 0.02:
        print("TYPING SPEED LEVEL: 4")
    if speed == 0.03:
        print("TYPING SPEED LEVEL: 3")
    if speed == 0.04:
        print("TYPING SPEED LEVEL: 2")
    if speed == 0.05:
        print("TYPING SPEED LEVEL: 1")
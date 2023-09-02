import psutil

# initial values
KEY_TYPING_SLEEP = 0.04
PERFECT_POS_X = 120.0
ADJUST_SPEED_AMOUNT = 0.25


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
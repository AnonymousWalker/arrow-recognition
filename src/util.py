import psutil

# initial values
KEY_TYPING_SLEEP = 0.03
PERFECT_POS_X = 120.0
ADJUST_SPEED_AMOUNT = 0.25


def get_pid_by_name(process_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    raise Exception("Audition is not running!")
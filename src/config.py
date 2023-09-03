from src.speed import bpm_speed_map

class Config:
        
    KEY_TYPING_SLEEP = 0.04
    PERFECT_POS_X = 120.0
    ADJUST_SPEED_AMOUNT = 0.25
    PIXELS_TO_PROCESS = 40.0
    ARROW_REGION = (150, 540, 720, 40) # extra-wide
    CURRENT_LEVEL = 5
    speed = bpm_speed_map[120]
    isFocused = True

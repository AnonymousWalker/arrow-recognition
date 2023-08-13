import cv2
import numpy as np


def get_head_position(template_image, main_image):
    # Finds the position of the playback head

    # Perform template matching
    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    template_height, template_width = template_image.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    center_x = (top_left[0] + bottom_right[0]) // 2
    center_y = (top_left[1] + bottom_right[1]) // 2

    print(center_x, center_y)
    # draw
    cv2.rectangle(main_image, top_left, bottom_right, (0, 255, 0), 1)

# Load the main image and the template image
# main_image = cv2.imread('resources/p3.png')
main_image = cv2.imread('resources/p1.png')
template = cv2.imread('resources/head.png')
get_head_position(template, main_image)

# Display the result
cv2.imshow('Object Detection', main_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

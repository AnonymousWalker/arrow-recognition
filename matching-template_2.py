import cv2
import numpy as np

# Load the template images for each arrow direction
template_up = cv2.imread('training-data/up/1.png', cv2.IMREAD_GRAYSCALE)
template_down = cv2.imread('training-data/down/1.png', cv2.IMREAD_GRAYSCALE)
template_left = cv2.imread('training-data/left/1.png', cv2.IMREAD_GRAYSCALE)
template_right = cv2.imread('training-data/right/1.png', cv2.IMREAD_GRAYSCALE)

# Load the input RGB image
input_image = cv2.imread('resources/2.jpg')
output_image = input_image.copy()

# Convert the input image to grayscale for template matching
gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# Perform template matching for each arrow direction
res_up = cv2.matchTemplate(gray_image, template_up, cv2.TM_CCOEFF_NORMED)
res_down = cv2.matchTemplate(gray_image, template_down, cv2.TM_CCOEFF_NORMED)
res_left = cv2.matchTemplate(gray_image, template_left, cv2.TM_CCOEFF_NORMED)
res_right = cv2.matchTemplate(gray_image, template_right, cv2.TM_CCOEFF_NORMED)

# Define a threshold for template matching results
threshold = 0.8

# Find the locations where the template matches with the input image
locations_up = np.where(res_up >= threshold)
locations_down = np.where(res_down >= threshold)
locations_left = np.where(res_left >= threshold)
locations_right = np.where(res_right >= threshold)

# Draw circles around the detected regions and label each arrow
for pt in zip(*locations_up[::-1]):
    cv2.putText(output_image, "U", (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

for pt in zip(*locations_down[::-1]):
    cv2.putText(output_image, "D", (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

for pt in zip(*locations_left[::-1]):
    cv2.putText(output_image, "L", (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

for pt in zip(*locations_right[::-1]):
    cv2.putText(output_image, "R", (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

# Display the output image
cv2.imshow('Detected Arrows', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

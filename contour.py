import cv2
import imutils
import numpy as np

def find_contours(image_path):
    # Read the image from the file
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply binary thresholding to create a binary image
    _, threshold_image = cv2.threshold(blurred_image, 100, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    cnts = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    return cnts

if __name__ == "__main__":
    # Provide the path to your image file
    # image_path = "resources/arr2.png"
    image_path = "resources/arrows.png"

    # Find contours in the image
    contours = find_contours(image_path)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])


    # Read the original image
    original_image = cv2.imread(image_path)

    # Iterate through contours, crop and save them as individual images
    for i, contour in enumerate(contours):
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # filter out images that aren't square-ish
        if abs(w - h) > 10 or h < 30 or w < 30:
            continue

        # Crop the region of interest (ROI) from the original image
        cropped_roi = original_image[y:y+h, x:x+w]

        # Save the cropped contour as an individual image
        output_path = f"out/cropped_contour_{i}.png"
        cv2.imwrite(output_path, cropped_roi)

    print("Cropped contour regions saved as individual images.")

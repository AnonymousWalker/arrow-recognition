import cv2
import imutils

def find_contours(image_path):
    # Read the image from the file
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply binary thresholding to create a binary image
    _, threshold_image = cv2.threshold(blurred_image, 150, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    cnts = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    return cnts

if __name__ == "__main__":
    # Provide the path to your image file
    image_path = "resources/bug/b2.png"
    # image_path = "resources/s1.png"

    # Find contours in the image
    contours = find_contours(image_path)

    # Draw the contours on the original image
    image_with_contours = cv2.imread(image_path)
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

    # Show the original image with contours
    cv2.imshow("Contours", image_with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
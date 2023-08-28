import cv2
import pytesseract

def detect_digit(image_path):
  # Read the image as grayscale
  image = cv2.imread(image_path, 0)

  # Apply Otsu's thresholding to binarize the image
  thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

  # Find contours in the binary image
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Find the largest contour, which should be the digit
  largest_contour = max(contours, key=cv2.contourArea)

  # Use Tesseract OCR to recognize the digit
  text = pytesseract.image_to_string(thresh, config='--psm 10')

  # Return the recognized digit
  return text

if __name__ == "__main__":
  # Image path
  image_path = "out/six.png"

  # Detect the digit
  digit = detect_digit(image_path)

  # Print the digit
  print(digit)

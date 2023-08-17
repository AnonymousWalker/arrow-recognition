import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import cv2

# arrow_directions = {
#     'up': 3,
#     'down': 0,
#     'left': 1,
#     'right': 2
# }
# output_class = ['down', 'left', 'right', 'up']
output_class = ['up', 'down', 'left', 'right']

# Load the trained model
model = load_model('trained-model/new_model.h5')  # Replace with the path to your trained model

def predict_direction(input_file):

    # Load and preprocess the input image
    input_image_path = input_file
    target_size = (28, 28)  # Make sure it matches the size your model expects

    # Open the image using PIL
    image = Image.open(input_image_path)

    # Resize and preprocess the image
    image = image.resize(target_size)
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(image)

    # Interpret the predictions
    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class
    # Here, you might need a class mapping to convert index to class label

    print("Predicted class:", output_class[predicted_class])

# for i in range(0, 8):
#     predict_direction('out/cropped_contour_{0}.png'.format(i))



def predict_direction2(input_cv2_image):

    # Preprocess the input image from cv2.imread
    target_size = (28, 28)  # Make sure it matches the size your model expects

    # Convert BGR image to RGB (since PIL uses RGB)
    input_image_rgb = cv2.cvtColor(input_cv2_image, cv2.COLOR_BGR2GRAY)

    # Resize and preprocess the image
    pil_image = Image.fromarray(input_image_rgb)
    image = pil_image.resize(target_size)
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(image)

    # Interpret the predictions
    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class
    # Here, you might need a class mapping to convert index to class label

    return output_class[predicted_class]



for i in range(1, 10):
    input_image_path = "resources/{0}.png".format(i)
    input_cv2_image = cv2.imread(input_image_path)

    # Use the modified function to make predictions
    d = predict_direction2(input_cv2_image)
    print(d)


# input_image_path = 'resources/3.png'
# input_cv2_image = cv2.imread(input_image_path)
# d = predict_direction2(input_cv2_image)
# print(d)
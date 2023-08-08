import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# arrow_directions = {
#     'up': 3,
#     'down': 0,
#     'left': 1,
#     'right': 2
# }
output_class = ['down', 'left', 'right', 'up']

# Load the trained model
model = load_model('trained-model/arrow_orientation_model.h5')  # Replace with the path to your trained model

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

for i in range(1, 11):
    predict_direction('resources/{0}.png'.format(i))


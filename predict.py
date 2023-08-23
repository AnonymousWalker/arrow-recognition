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
# output_class = ['up', 'down', 'left', 'right']
output_class = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right', 'unknown']

# Load the trained model

def predict_direction_1(input_cv2_image):
    model = load_model('trained-model/model_v1.h5')  # Replace with the path to your trained model

    target_size = (28, 28)  # Make sure it matches the size your model expects

    # Open the image using PIL
    image = cv2.cvtColor(input_cv2_image, cv2.COLOR_BGR2RGB)

    # Resize and preprocess the image
    image = image.resize(target_size)
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(image)

    # Interpret the predictions
    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class
    # Here, you might need a class mapping to convert index to class label
    _output_class = ['down', 'left', 'right', 'up']
    print("Predicted class:", _output_class[predicted_class])

# for i in range(0, 8):
#     predict_direction('out/cropped_contour_{0}.png'.format(i))



def predict_direction2(input_cv2_image):
    model = load_model('trained-model/8k_rgb_v2.1.h5')  # Replace with the path to your trained model

    # Preprocess the input image from cv2.imread
    target_size = (28, 28)  # Make sure it matches the size your model expects

    input_image_converted = cv2.cvtColor(input_cv2_image, cv2.COLOR_BGR2RGB)

    # Resize and preprocess the image
    pil_image = Image.fromarray(input_image_converted)
    image = pil_image.resize(target_size)
    image = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(image)

    # Interpret the predictions
    print(np.max(predictions))
    if np.max(predictions) < 0.8:
        return 'unknown'
    
    predicted_class = np.argmax(predictions)  # Get the index of the highest probability class
    # Here, you might need a class mapping to convert index to class label

    return output_class[predicted_class]



# res = []
# for i in range(1, 18):
#     input_image_path = "resources/manual-testing/_ ({0}).png".format(i)
#     input_cv2_image = cv2.imread(input_image_path)

#     # Use the modified function to make predictions
#     d = predict_direction2(input_cv2_image)
#     res.append(d)

# print(res)


input_image_path = 'out/cropped_contour_8.png'
input_cv2_image = cv2.imread(input_image_path)
d = predict_direction2(input_cv2_image)
print(d)
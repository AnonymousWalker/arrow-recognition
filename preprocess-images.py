from PIL import Image
import os

# Define the arrow directions and corresponding class labels
arrow_directions = {
    'up': 0,
    'down': 1,
    'left': 2,
    'right': 3
}

# Resize images to 28x28 pixels and convert to grayscale
def preprocess_image(image_path):
    img = Image.open(image_path)#.convert('L')  # Convert to grayscale
    img = img.resize((28, 28))
    return img

# Specify the root directory containing arrow direction subdirectories
root_dir = 'training-data'
output_dir = 'out/resized_arrows'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each arrow direction subdirectory
for direction, label in arrow_directions.items():
    direction_dir = os.path.join(root_dir, direction)
    
    # Process each image in the direction subdirectory
    for filename in os.listdir(direction_dir):
        if filename.endswith('.png'):
            input_path = os.path.join(direction_dir, filename)
            output_path = os.path.join(output_dir, direction, filename)
            
            # Preprocess the image and save the resized version
            resized_image = preprocess_image(input_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            resized_image.save(output_path)

print("Images resized and saved to the output directory.")

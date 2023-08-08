from PIL import Image

# Path to the input image
input_image_path = 'test-data/6.png'  # Replace with your image file path

# Path to save the resized image
output_image_path = 'test-data/left/2.png'  # Replace with desired output path

# Open the image using PIL
image = Image.open(input_image_path)

# Resize the image
target_size = (28, 28)
resized_image = image.resize(target_size)  # Using Lanczos resampling

# Save the resized image
resized_image.save(output_image_path)

print("Image resized and saved successfully!")

from PIL import Image

# Load the RGBA image
input_image_path = 'path_to_input_image.png'  # Replace with the path to your input image
output_image_path = 'path_to_output_image.jpg'  # Replace with the desired output path

# Open the image using PIL
image_rgba = Image.open('resources/9.png')

# Convert RGBA to RGB
image_rgb = image_rgba.convert('RGB')

# Save the converted image
image_rgb.save('resources/9-rgb.png')

print("Image converted and saved successfully!")

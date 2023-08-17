from PIL import Image
import os
# # Path to the input image
# input_image_path = 'test-data/6.png'  # Replace with your image file path

# # Path to save the resized image
# output_image_path = 'test-data/left/2.png'  # Replace with desired output path

# # Open the image using PIL
# image = Image.open(input_image_path)

# # Resize the image
# target_size = (28, 28)
# resized_image = image.resize(target_size)  # Using Lanczos resampling

# # Save the resized image
# resized_image.save(output_image_path)

# print("Image resized and saved successfully!")



# BATCH RESIZE
def resize_images(source_folder, target_folder, new_size):
    counter = 1

    for filename in os.listdir(source_folder):
        if filename.endswith('.png'):
            try:
                source_path = os.path.join(source_folder, filename)
                img = Image.open(source_path)
                img = img.resize(new_size)

                target_path = os.path.join(target_folder, f"{counter}.png")
                img.save(target_path)
                counter += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")

source_folder = "resources/8k-split/UP-RIGHT"
target_folder = "training-data/resized_arrows_8k/up-right"
new_size = (28, 28)

resize_images(source_folder, target_folder, new_size)
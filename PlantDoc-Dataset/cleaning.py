from PIL import Image
import imagehash
import os

# Directory containing the images
image_dir = 'D:/Riya/Capstone/PlantDoc-Dataset/train/Tomato two spotted spider mites leaf'

# Dictionary to store hashes of images
hashes = {}

# Iterate over each image file
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Open the image and compute its hash
        with Image.open(os.path.join(image_dir, filename)) as img:
            hash_value = imagehash.dhash(img)
        # Store the hash value in the dictionary
        if hash_value in hashes:
            hashes[hash_value].append(filename)
        else:
            hashes[hash_value] = [filename]

# Identify duplicate images
duplicate_images = []
for hash_value, filenames in hashes.items():
    if len(filenames) > 1:
        duplicate_images.extend(filenames)

# Print duplicate images
print("Duplicate Images:")
for filename in duplicate_images:
    print(filename)

# Optionally, remove or mark duplicate images

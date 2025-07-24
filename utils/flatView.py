import os
from PIL import Image

def merge_images(directory):
    """
    Merge satellite images in the given directory into a single image.

    Args:
        directory (str): The directory where the satellite images are located.
    """
    # Create a list to store the satellite image paths
    image_paths = []

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            image_paths.append(os.path.join(directory, filename))

    # Sort the image paths in descending order
    image_paths.sort(reverse=True)

    # Create a list to store the image objects
    images = []

    # Open each image and append it to the list
    for image_path in image_paths:
        image = Image.open(image_path)
        images.append(image)

    # Create a new blank image with the same size as the first image
    merged_image = Image.new('RGBA', images[0].size, (40, 77, 166))

    # Layer each image on top of the merged image with an offset of -2, -2 px
    offset = (0, 0)
    for image in images:
        merged_image.paste(image, offset, image)
        offset = (offset[0] - 2, offset[1] - 2)

    # Save the merged image as 'map1.png'
    merged_image.save('utils/map_merged.png')

# Merge the satellite images in the 'satellite_images' directory
merge_images('tibia_15.10.77ba00')
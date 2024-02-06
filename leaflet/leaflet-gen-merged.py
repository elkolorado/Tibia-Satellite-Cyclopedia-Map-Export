from PIL import Image
import os

# Open the image
image = Image.open('utils/map_merged.png')

# Define the tile size
tile_size = 512

# Get the width and height of the image
width, height = image.size

# Calculate the number of tiles in x and y directions
num_tiles_x = width // tile_size
num_tiles_y = height // tile_size

# Iterate over each tile
# Create the "leaflet" directory if it doesn't exist
if not os.path.exists("leaflet"):
    os.makedirs("leaflet")

for x in range(num_tiles_x):
    for y in range(num_tiles_y):
        # Calculate the coordinates of the current tile
        left = x * tile_size
        upper = y * tile_size
        right = left + tile_size
        lower = upper + tile_size

        # Crop the image to the current tile
        tile = image.crop((left, upper, right, lower))

        # Save the tile with the appropriate filename in the "leaflet" directory
        tile_filename = f'leaflet/merged/map_merged_{x}_{y}.png'
        tile.save(tile_filename)

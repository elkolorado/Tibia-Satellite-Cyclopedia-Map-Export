import os
import re
import lzma
from PIL import Image
import io
import sys
import os
import argparse

def process_image(directory, image_width=512, image_height=512, output_file='map', floor=7, output_directory=None):
    """
    Process satellite images in a directory and create a large composite image.

    Args:
        directory (str): The directory containing the satellite images.
        image_width (int, optional): The width of each individual image in pixels. Defaults to 512.
        image_height (int, optional): The height of each individual image in pixels. Defaults to 512.
        output_file (str, optional): The name of the output file. Defaults to 'map'.
        floor (int, optional): The floor level of the satellite images. Defaults to 7.
        output_directory (str, optional): The directory to save the output file. Defaults to None.
    """
    # Initialize the minimum X and Y coordinates
    min_x = min_y = float('inf')
    # Initialize the maximum X and Y coordinates
    max_x = max_y = float('-inf')

    search_pattern = rf'satellite-16-(\d+)-(\d+)-0{floor}-'

    # Scan the directory to find the minimum X and Y coordinates
    for filename in os.listdir(directory):
        # Check if the file is a .bmp.lzma file
        if filename.endswith('.bmp.lzma'):
            # Extract the X and Y coordinates from the filename
            match = re.search(search_pattern, filename)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))

                # Update the minimum X and Y coordinates
                min_x = min(min_x, x)
                min_y = min(min_y, y)

                # Update the maximum X and Y coordinates
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    # Calculate the number of images in the x and y directions
    num_images_x = (max_x - min_x) // 8 + 1
    num_images_y = (max_y - min_y) // 8 + 1

    # Create a new blank image
    large_image = Image.new('RGBA', (image_width * num_images_x, image_height * num_images_y))

    # Scan the directory again to process the images
    for filename in os.listdir(directory):
        # Check if the file is a .bmp.lzma file
        if filename.endswith('.bmp.lzma'):
            # Extract the X and Y coordinates from the filename
            match = re.search(search_pattern, filename)
            if match:
                x = (int(match.group(1)) - min_x) // 8
                y = (int(match.group(2)) - min_y) // 8

                # Open the LZMA-compressed BMP file
                with open(os.path.join(directory, filename), 'rb') as file:
                    # Read the compressed data
                    compressed_data = bytearray(file.read())

                # Skip the first 32 bytes
                compressed_data = compressed_data[32:]

                # Modify the header to set the uncompressed size to the maximum value
                for i in range(5, 13):
                    compressed_data[i] = 0xFF

                # Decompress the data
                decompressed_data = lzma.decompress(compressed_data)

                # Create an in-memory stream from the decompressed data
                stream = io.BytesIO(decompressed_data)

                # Open the BMP image using PIL
                bmp_image = Image.open(stream)

                # Convert the BMP image to PNG format
                png_image = bmp_image.convert('RGBA')

                # Paste the PNG image onto the large image at the correct position
                large_image.paste(png_image, (x * image_width, y * image_height))

    if output_directory is not None:
        if not os.path.isabs(output_directory):
            output_directory = os.path.join(os.getcwd(), output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        output_path = os.path.join(output_directory, f'{output_file}{floor}.png')
    else:
        output_path = f'{output_file}{floor}.png'
    large_image.save(output_path)

def requestMap(directory, output_file='map', floor=None, output_directory=None):
    if floor is not None:
        print(f'Processing floor {floor}')
        process_image(directory, output_file=output_file, floor=floor, output_directory=output_directory)
        print(f'Finished processing floor {floor} to {output_directory}')
    else:
        for floor in range(8):
            print(f'Processing floor {floor}')
            process_image(directory, output_file=output_file, floor=floor, output_directory=output_directory)
            print(f'Finished processing floor {floor}')

def parse_arguments():
    
    parser = argparse.ArgumentParser(description='Script for processing satellite images.')
    parser.add_argument('directory', metavar='DIRECTORY', type=str, nargs='?', default=None,
                        help='the directory containing the satellite images in your Tibia/assets')
    parser.add_argument('-o', '--output', metavar='OUTPUT_FILE', type=str, default='map',
                        help='the output file name (default: map)')
    parser.add_argument('-f', '--floor', metavar='FLOOR', type=int, default=None,
                        help='the floor number to process (default: all floors)')
    parser.add_argument('-d', '--output-directory', metavar='OUTPUT_DIRECTORY', type=str, default=None,
                        help='the directory to save the output file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    directory = args.directory
    output_file = args.output
    floor = args.floor
    output_directory = args.output_directory

    if directory is None:
        appdata_path = os.path.expandvars('%LOCALAPPDATA%')
        directory = os.path.join(appdata_path, 'Tibia', 'packages', 'Tibia', 'assets')

    requestMap(directory, output_file=output_file, floor=floor, output_directory=output_directory)

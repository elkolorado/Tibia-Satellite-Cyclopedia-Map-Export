# Tibia Cyclopedia Map

[Online Viewer](https://elkolorado.github.io/tibialibraries/cyclopediamap/)

This script is used for processing satellite images in the Tibia game. It generates a satellite map view of each floor.

Tibia uses `.bmp.lzma` files to store chunked satellite view in Cyclopedia Map.

After skipping the first 32 bytes and modifying the header to set the uncompressed size to the maximum value, you can decompress the remaining data to obtain the original satellite view.

```py
# Read the compressed .bmp.lmza file into bytearray
compressed_data = bytearray(file.read())

# Skip the first 32 bytes
compressed_data = compressed_data[32:]

# Modify the header to set the uncompressed size to the maximum value
for i in range(5, 13):
    compressed_data[i] = 0xFF

# Decompress the data
decompressed_data = lzma.decompress(compressed_data)
```

The calculation for map size was done assuming the 512x512 original decompressed size.

# Usage

To use the script, follow these steps:

1. Install the necessary dependencies by running `pip install -r requirements.txt`.
2. Run the script with the following command:

   ```bash
   python satellite.py
    ```

    Or with params
   ```bash
   python satellite.py [DIRECTORY] [-d OUTPUT_DIRECTORY] [-o OUTPUT_FILE] [-f FLOOR] 
   ```
3. The script accepts the following parameters:

- `DIRECTORY`: The directory containing the satellite images in your Tibia/assets. This is an optional parameter. If not provided, the script will use the default directory.

- `-o OUTPUT_FILE`, `--output OUTPUT_FILE`: The output file name. This is an optional parameter. The default value is "map".

- `-f FLOOR`, `--floor FLOOR`: The floor number to process. This is an optional parameter. If not provided, the script will process all floors.

- `-d OUTPUT_DIRECTORY`, `--output-directory OUTPUT_DIRECTORY` The directory to save the output file. This is an optional parameter. If not provided, the script will use the current working directory.
  
- `-l`, `--loseless` This is optional paramter. If provided, the result will be saved as original .bmp file. By default the map is saved as compressed .png

To use the script, you can run it with the following command:

# Examples

Render all floors, into cwd directory
   ```bash
   python satellite.py
   ```
    
Render just the floor 0 map, into `export` directory
   ```bash
   python satellite.py -d export -f 0
   ```
    

       

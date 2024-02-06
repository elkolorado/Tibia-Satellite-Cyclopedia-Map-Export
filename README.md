# Tibia Cyclopedia Map

This script is used for processing satellite images in the Tibia game. It generates a map based on the images found in the specified directory.

## Usage

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

To use the script, you can run it with the following command:

4. Example

   ```bash
   python satellite.py -d export -f 0
   ```
    
   Will render just the floor 0 map, into export directory
       

import os
import tiffile
from preprocess import preprocessing
import logging
import json


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Define CONFIG_PATH relative to this file's location
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config(config_path="config.json"):
    with open(config_path, "r") as config_file:
        return json.load(config_file)
    
def main():

    # Extract paths from config
    config = load_config(CONFIG_PATH)

    path_settings = config["Path_settings"]

    # Preprocess raw data (split channels + max projection)
    logging.info("Starting preprocessing of raw images...")
    image_stacks_dict = preprocessing(path_settings) 
    logging.info("Preprocessing completed. Proceed with the segmentation")


if __name__ == '__main__':
    main()

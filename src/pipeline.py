import os
import tiffile
from preprocess import preprocessing
from load_data import load_preprocessed_data
from segmentation import load_segmentation_mask
from analysis import processing
from plots import plot_copy_number_distribution
from stats import compute_stats
from save_metadata import save_full_metadata
import logging
import json
import numpy as np

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

    Path_settings = config["Path_settings"]
    Plot_settings = config["Plot_settings"]
    output_dir = Path_settings["output_dir"]

    # Step 1: Loading the preprocessed data 
    logging.info("Loading GFP and RFP stacks...")
    image_stacks_dict = load_preprocessed_data(Path_settings)
    if not image_stacks_dict:
        logging.error("No image stacks were loaded. Aborting processing.")
        raise ValueError("Empty image_stacks dictionary.")
    else:
        logging.info("Loading GFP and RFP stacks completed.")

    # Step 2: Load segmentation masks
    logging.info("Loading segmentation masks...")
    masks_dict = load_segmentation_mask(Path_settings)
    if not masks_dict:
        logging.error("Loading masks failed.")
        raise ValueError("Segmentation resulted in an empty dataset.")
    logging.info(f"Loaded {len(masks_dict)} masks. Moving to processing.")


    # step 3: Processing the data
    logging.info("Processing started...")
    final_processed_data = processing(image_stacks_dict, masks_dict, config)
    logging.info(f"Processing completed successfully for {len(final_processed_data)} cells.")

    # step 4: Plots ans Stats
    copy_numbers = np.array(final_processed_data['Copy Number'])
    if config['stats_summary']:
        logging.info('Providing stats summary')
        compute_stats(copy_numbers, output_dir)

    if config['plot_copy_number']:
        logging.info('starting the plotting of copy number')
        plot_copy_number_distribution(copy_numbers, output_dir, Plot_settings)

    # step 5: save metadata 
    logging.info(f"Saved metadata to: {output_dir}")
    save_full_metadata(config, output_dir)




if __name__ == '__main__':
    main()

    





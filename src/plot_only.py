import os
import logging
import json
from plots import plot_copy_number_distribution
import pandas as pd
import numpy as np
from save_metadata import save_full_metadata



# set up logging configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# Define CONFIG_PATH relative to this file's location
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config(config_path = CONFIG_PATH):
    with open(config_path, "r") as f:
        return json.load(f)


def main():
    logging.info("Loading configuration...")
    config = load_config(CONFIG_PATH)
    path_settings = config["Path_settings"]
    plot_settings = config["Plot_settings"]
    output_path = os.path.join(path_settings["output_dir"], path_settings["output_name"])

    # Check if the processed data file exists
    if not os.path.exists(output_path):
        logging.error(f"Processed data file not found at {output_path}. Please run the full pipeline first.")
        return

    logging.info(f"loading the data from {output_path}...")
    processed_data = pd.read_csv(output_path)

    if 'Copy Number' not in processed_data.columns:
        logging.error("'Copy Number' column not found in processed data. Aborting.")
        return
    
    copy_numbers = np.array(processed_data['Copy Number'])

    if copy_numbers.size == 0:
        logging.error("No copy number data found. Aborting plot.")
        return
    # generating the plot

    logging.info("plotting the copy number distribution...")
    plot_copy_number_distribution(copy_numbers, path_settings["output_dir"], plot_settings)
    logging.info("Plotting completed successfully.")


    # save the metadata 
    output_dir = path_settings["output_dir"]
    logging.info(f"Saved metadata to: {output_dir}")
    save_full_metadata(config, output_dir)


if __name__ =='__main__':
    main()

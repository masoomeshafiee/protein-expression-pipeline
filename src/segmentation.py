import os
import logging 
import imageio.v2 as imageio
import numpy as np
from tqdm import tqdm


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("pipeline.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to the console
    ]
)


def load_segmentation_mask(Path_settings):
    """"
    Load the segmented mask done by cellpose (.png) corresponding to the given filename. The background is 0 and each cell has a unique number in the mask. 

    Args:
    Path_settings (config dict):
        mask_dir (str): Path to the segmentation mask directory. (Note: the segmentation was done from the GFP projection)
        input dir (str): path to the raw data
        mask_siffix(str): for the mask file name

    
    Returns:
        np.ndarray: Loaded mask image as an integer array, or None if loading fails.
        - masks(dict):dictionary with the file names as keys and segmentation masks (np.ndarray integer array) as values.
    """
    input_dir = Path_settings["input_dir"]
    mask_dir = Path_settings["mask_dir"]
    mask_suffix = Path_settings["mask_suffix"]

    masks = {}
    for filename in tqdm(os.listdir(input_dir)):
        if filename.endswith(".TIF"):
            mask_filename = filename.replace('.TIF', mask_suffix)
            mask_path = os.path.join(mask_dir,mask_filename)

        if not os.path.exists(mask_path):
            logging.warning(f"Segmentation mask not found: {mask_path}")
            continue
    
        try:
            mask = imageio.imread(mask_path)
            mask = np.array(mask, dtype=np.uint16)
            
            unique_values = np.unique(mask)
            masks[filename] = mask
            logging.info(f"Loaded mask: {mask_filename}, number of cells: {len(unique_values) - 1}")

        
        except Exception as e:
            logging.error(f"failed to load the masks {mask_path}: {e}")
            continue
    
    return masks
    



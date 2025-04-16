import os
import logging 
from tqdm import tqdm
import tiffile


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("pipeline.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to the console
    ]
)


def load_preprocessed_data(Path_settings):
    """"
    Loads the GFP and RFP stacks corresponding tp each field of view.

    Args: 
    path_settings (config dict):
        input dir (str): path to the raw data - to access the file names.
        GFP_dir: path to GFP stacks.
        RFP_dir: path to RFP stacks. 
        GFP_suffix in the file name in GFP directory
        RFP_suffix in the file name in RFP directory

    
    Returns:
        - image_stacks_dict(dict):  dictionary with the file names as keys and a dict:{'GFP': GFP_stack, 'RFP': RFP_stack} as values. 
    """
    input_dir = Path_settings["input_dir"]
    GFP_dir = Path_settings["GFP_dir"]
    RFP_dir = Path_settings["RFP_dir"]
    GFP_suffix = Path_settings["GFP_suffix"]
    RFP_suffix = Path_settings["RFP_suffix"]
    
    image_stacks_dict = {}
    for file_name in tqdm(os.listdir(input_dir)):
        # Skip hidden files like .DS_Store:
        if file_name.startswith('.'):
            continue
        if file_name.endswith(".TIF"):
            GFP_filename = file_name.replace('.TIF', GFP_suffix)
            GFP_path = os.path.join(GFP_dir,GFP_filename)

            RFP_filename = file_name.replace('.TIF', RFP_suffix)
            RFP_path = os.path.join(RFP_dir,RFP_filename)

        if not os.path.exists(GFP_path):
            logging.warning(f"GFP stack not found: {GFP_path}")
            continue

        if not os.path.exists(RFP_path):
            logging.warning(f"RFP stack not found: {RFP_path}")
            continue
    
        try:
            #read the GFP stacks
            GFP_stack = tiffile.imread(GFP_path)
            logging.info(f"Loaded GFP: {GFP_filename}")
            
            #read the RFP stacks
            RFP_stack = tiffile.imread(RFP_path)
            logging.info(f"Loaded RFP: {RFP_filename}")

            image_stacks_dict[file_name] = {'GFP': GFP_stack, 'RFP': RFP_stack}
            
        except Exception as e:
            logging.error(f"failed to load the GFP or RFP stack for{file_name}: {e}")
            continue

    
    return image_stacks_dict
    

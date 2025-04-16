import os
from tqdm import tqdm
import numpy as np
import tifffile
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("pipeline.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to the console
    ]
)

def split_image_stack(image_stack):
    """
    Split each slice in the z-stack into two halves (RFP and GFP).
    """
    GFP_stack = []
    RFP_stack = []

    for image in image_stack:
        middle_col = image.shape[1]//2
        # Split each slice into RFP and GFP
        RFP_stack.append(image[:,:middle_col]) # Left half for RFP
        GFP_stack.append(image[:,middle_col:]) # Right half for GFP
    
    # Convert the lists into numpy arrays (3D stacks)
    RFP_stack = np.array(RFP_stack)
    GFP_stack = np.array(GFP_stack)

    return RFP_stack, GFP_stack

def max_projection(GFP_stack):
    """
    Perform max projection along the z-axis (3rd axis) to get a 2D image.
    """
    return np.max(GFP_stack, axis = 0)

def save_image(image, file_name, save_dir, suffix):
    """
    Save any image (RFP stack, GFP stack, GFP projection) to the specified directory.
    """
    file_path = os.path.join(save_dir, file_name.replace('.TIF', suffix))
    try:    
        tifffile.imwrite(file_path, image)
        logging.info(f"Saved: {file_path}")
    except:
        logging.error(f"Failed to save {file_path}: {e}")


def preprocessing(path_settings):
     """
    Preprocess the images: split the dual channels and create max projections for GFP (to be used for segmentation).

    saves the reults into GFP and RFP directory and the projection directory.

    """
     input_dir = path_settings["input_dir"]
     GFP_dir = path_settings["GFP_dir"]
     RFP_dir = path_settings["RFP_dir"]
     projected_dir = path_settings["projected_dir"]
     GFP_suffix = path_settings["GFP_suffix"]
     RFP_suffix = path_settings["RFP_suffix"]
     projection_suffix = path_settings["projection_suffix"]

     os.makedirs(GFP_dir, exist_ok=True)
     os.makedirs(RFP_dir, exist_ok=True)
     os.makedirs(projected_dir, exist_ok=True)
     for file_name in tqdm(os.listdir(input_dir)):
        if file_name.endswith(".TIF") or file_name.endswith(".tif") :
            file_path = os.path.join(input_dir, file_name)
            try: 
                #read the image stacks
                image_stack = tifffile.imread(file_path)

                # Split the image stack into RFP and GFP channels
                RFP_stack, GFP_stack = split_image_stack(image_stack)

                # Create max projection of GFP stack
                GFP_projection = max_projection(GFP_stack)

                # Save the results (split stacks and max projection)
                save_image(GFP_stack, file_name, GFP_dir, GFP_suffix)
                save_image(RFP_stack, file_name, RFP_dir, RFP_suffix)
                save_image(GFP_projection, file_name,projected_dir, projection_suffix)

            except Exception as e:
                logging.error(f"Error processing {file_name}: {e}")

     logging.info("Preprocessing completed successfully.")


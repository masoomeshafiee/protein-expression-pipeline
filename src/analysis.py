import numpy as np
import matplotlib.pyplot as plt
import logging
import pandas as pd
import os

#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def segment_stacks(image_stacks, masks):
    """"
    Segments the GFP and RFP stacks using the corresponding masks.

    Parameters:
    - image_stacks (dict): dictionary with the file names as keys and dicts of 'GFP' and 'RFP' stacks as values.
    - masks(dict):dictionary with the file names as keys and segmentation masks as values.
    
    Returns:
    - sgmented_data (dict): dictionary storing the segmented GFP and RFP stacks for each file and cell ID.
    
    """

    segmented_data = {}

    for file_name, channels in image_stacks.items():
        if file_name in masks:
            mask = masks[file_name]
            unique_cell_ids = np.unique(mask)
            unique_cell_ids = unique_cell_ids[unique_cell_ids != 0] # Exclude background
            unique_cell_ids = [int(cell_id) for cell_id in unique_cell_ids]  # Convert to native int
            if len(unique_cell_ids)==0:
                logging.warning(f'{file_name} does not contain any cell')
                continue

            segmented_data[file_name] = {}

            for cell_id in unique_cell_ids:

                binary_mask = (mask == cell_id).astype(np.uint8)

                segmented_GFP_stack = np.array([image * binary_mask for image in channels['GFP']])
                segmented_RFP_stack = np.array([image * binary_mask for image in channels['RFP']])

                segmented_data[file_name][cell_id] = {'GFP': segmented_GFP_stack, 'RFP': segmented_RFP_stack}
                
                logging.info(f'sucsussfuly segmented the cell {cell_id} in the {file_name}')
        else: 
            logging.warning(f'mask was not found for {file_name} file')
    
    return segmented_data

def find_active_slices(segmented_data, active_slice_settings):
    """
    Finds active slices for each cell based on intensity drop in the GFP channel.

    Args:
        segmented_data (dict): Dictionary containing {file_name: {cell_id: {'GFP': array, 'RFP': array}}}
        active_slice_settings: configuration for the drop intensity threishold

    Returns:
        dict: Dictionary with {file_name: {cell_id: {'Focal Slice': int, 'Focal Intensity': float, 
        'Threshold Intensity': float, 'Active Slices': list}}}
    """
    drop_threshold = active_slice_settings["drop_threshold"]
    plot_intensity_profile = active_slice_settings["plot_intensity_profile"] # wether plot the intensity profile of each cell or not


    active_slices_dict = {}

    for file_name, cells in segmented_data.items():
        active_slices_dict[file_name] = {}

        for cell_id, channels in cells.items():

            if not 'GFP' in channels:
                logging.warning(f'Skipping cell {cell_id} in the file {file_name}: No GFP file found.')

            # extracting GFP stack for the current cell
            GFP_stack = channels['GFP'] 

            # Compute sum of pixel intensities for each slice
            intensity_sums = [np.sum(image) for image in GFP_stack] 

            # Identify focal slice (slice with max intensity)
            focal_plane = int(np.argmax(intensity_sums))
            focal_intensity = float(intensity_sums[focal_plane])

            # Define threshold intensity
            threshold_intensity = focal_intensity * (1 - drop_threshold / 100)

            # Identify active slices
            active_slices = [i for i, intensity in enumerate(intensity_sums) if intensity >= threshold_intensity]

            #store the results
            active_slices_dict[file_name][cell_id] = { 'focal slice': focal_plane, 'focal intensity': focal_intensity,'threshold intensity': threshold_intensity,'active slices': active_slices}

            logging.info(f'Extracted the active slices for the cell {cell_id} in the file {file_name} Focal Slice={focal_plane}, Active Slices={active_slices}')
                          
            # Optional: Plot intensity profile
            if plot_intensity_profile:
                plt.figure(figsize=(10, 6))
                plt.plot(intensity_sums, label='Intensity Profile')
                plt.axhline(y=threshold_intensity, color='r', linestyle='--', label='Threshold Intensity')
                plt.axvline(x=focal_plane, color='g', linestyle='--', label='Focal Slice')
                plt.xticks(ticks=np.arange(len(intensity_sums)), labels=np.arange(len(intensity_sums)))
                plt.title(f"Intensity Profile for Cell {cell_id} in {file_name}")
                plt.xlabel('Slice Number')
                plt.ylabel('Sum of Intensities')
                plt.legend()
                plt.show()
            

    logging.info(f' Sucsussfully extracted the active slices for all the cells. Proceeding with copy number calculation.')
    return active_slices_dict

def cell_intensity(segmented_data, active_slices_dict, analysis_settings):
    """
    Computes total cell intensity, which is normalized for cell autofourescent. 

    Args:
        - segmented_data (dict): Dictionary containing {file_name: {cell_id: {'GFP': array, 'RFP': array}}}
        - active_slices_dict (dict):Dictionary with {file_name: {cell_id: {'Focal Slice': int, 'Focal Intensity': float, 
        'Threshold Intensity': float, 'Active Slices': list}}}
        - analysis_settings (config dict):
        rg (float): GFP scaling factor for autofluorescence correction.
        ra (float): RFP scaling factor for autofluorescence correction.
        single_mNG_intensity (float): Intensity of a single mNeonGreen molecule for copy number estimation.

    Returns:
        processed_data (dict): Processed data containing calculated intensities and copy numbers for each cell in each file.
    """
    ra = analysis_settings["ra"]
    rg = analysis_settings["rg"]
    single_mNG_intensity = analysis_settings["single_mNG_intensity"]

    processed_intensity_data = {}


    for file_name, cells in segmented_data.items():
        
       processed_intensity_data[file_name] = {}

       for cell_id, channels in cells.items():
           
           # Extract the GFP and RFP stacks
           gfp_stack = channels['GFP']
           rfp_stack = channels['RFP']

           # Get the active slices from active_slices_data
           active_slices = active_slices_dict.get(file_name, {}).get(cell_id, {}).get('active slices', [])
           # Calculate total intensity of the cell in each channel
           gfp_total_intensity = sum(np.sum(gfp_stack[i]) for i in active_slices)
           rfp_total_intensity = sum(np.sum(rfp_stack[i]) for i in active_slices)

           # calculate the normalized intensity
           total_intensity_normal = (rg * gfp_total_intensity - ra * rg * rfp_total_intensity) / (rg - ra)
           copy_number = total_intensity_normal / single_mNG_intensity

           processed_intensity_data[file_name][cell_id] = {'total_intensity': gfp_total_intensity,
                'total_background': rfp_total_intensity,
                'total_intensity_normal': total_intensity_normal,
                'copy_number': copy_number}
           logging.info(f'Calculated the copy number for the cell {cell_id} in the file {file_name}')
           
    logging.info(f'Copy number calculation was done.')
    return processed_intensity_data

def save_processed_data(active_slices_dict, processed_intensity_data, output_path):
    """
    Merge all the processed info resulted from different functions.

    Args:
        active_slices_dict (dict): Dictionary with structure:
            {file_name: {cell_id: {
                'Focal Slice': int,
                'Focal Intensity': float,
                'Threshold Intensity': float,
                'Active Slices': list
            }}}
        processed_intensity_data (dict): Dictionary with structure:
            {file_name: {cell_id: {
                'total_intensity': float,
                'total_background': float,
                'total_intensity_normal': float,
                'copy_number': float
            }}}
        output_path (str): path to save the processed data into a csv file.
    Return:
        df (pandas dataframe): intenisty values and active slice information for each cell in each datafile.

    
    """
    # Initialize a list to store flattened rows
    flattened_data = []

    logging.info("Saving data.")

    for file_name, cells in active_slices_dict.items():
        for cell_id, active_slice_info in cells.items():
            # Retrieve intensity data
            intensity_values = processed_intensity_data.get(file_name, {}).get(cell_id, {})

            logging.debug(f"Processing cell {cell_id} in file {file_name} - Active Slice Info: {active_slice_info}")
            logging.debug(f"Processing cell {cell_id} in file {file_name} - Intensity Values: {intensity_values}")

            # Merge active slice info and intensity data
            row = {
                'File Name': file_name,
                'Cell ID': cell_id,
                'Focal Slice': active_slice_info.get('focal slice', None),
                'Focal Intensity': active_slice_info.get('focal intensity', None),
                'Threshold Intensity': active_slice_info.get('threshold intensity', None),
                'Active Slices': ', '.join(map(str, active_slice_info.get('active slices', []))),
                'Total Intensity': intensity_values.get('total_intensity', None),
                'Total Background': intensity_values.get('total_background', None),
                'Total Intensity Normal': intensity_values.get('total_intensity_normal', None),
                'Copy Number': intensity_values.get('copy_number', None)
            }
            logging.debug(f"Row data for cell {cell_id} in file {file_name}: {row}")
            flattened_data.append(row)
    # convert to dataframe
    df = pd.DataFrame(flattened_data)
    logging.info("Data successfully flattened into DataFrame.")

    # save as a CSV file
    try: 
        df.to_csv(output_path,index=False)
        logging.info(f"Successfully saved the processed data to {output_path}.")
    except Exception as e:
        logging.error(f"Error while saving CSV file: {e}")
        raise

    return df

def processing(image_stacks, masks, config):
    """
    1. Segments the GFP and RFP stacks using the corresponding masks.
    2. Finds focal plane and the active slices for each cell.
    3. Calculates the total intensity for each cell and corrects the autoflourescent background.
    4. Calculates the copy numebr for each cell.

    Parameters:
    - image_stacks (dict): dictionary with the file names as keys and dicts of 'GFP' and 'RFP' stacks as values.
    - masks(dict):dictionary with the file names as keys and segmentation masks as values.

    retunrs: 
    final_processed_data (dict): for each file and each cell inside the file: Focal Slice, Focal Intensity, Threshold Intensity, Active Slices
    total_intensity, total_background, total_intensity_normal, copy_number

    """
    Path_settings = config["Path_settings"]
    output_path = os.path.join(Path_settings["output_dir"],Path_settings["output_name"])
    active_slice_settings = config["active_slice_settings"]
    analysis_settings = config["Analysis_settings"]
    
    
    # 1. segmenting the GFP and RFP stacks for each file and cell ID
    segmented_data = segment_stacks(image_stacks, masks)
    if not segmented_data:
        logging.error("No cells were segmented. Aborting processing.")
        raise ValueError("Segmentation resulted in an empty dataset.")

    # 2. finding the active slices for each cell
    active_slices_dict = find_active_slices(segmented_data, active_slice_settings)
    if not any(active_slices_dict[file] for file in active_slices_dict):
        logging.error("No active slices found for any cells. Aborting processing.")
        raise ValueError("Active slice extraction failed.")

    # 3. Calculating the copy number for each cell
    processed_intensity_data = cell_intensity(segmented_data, active_slices_dict, analysis_settings)
    if not any(processed_intensity_data[file] for file in processed_intensity_data):
        logging.error("No intensity data calculated. Aborting processing.")
        raise ValueError("Intensity calculation resulted in no data.")

    # 4. Merging the all the extracted information and saving it to csv file
    final_processed_data = save_processed_data(active_slices_dict, processed_intensity_data, output_path)
    if final_processed_data.empty:
        logging.error("Merging completed, but final dataset is empty.")
        raise ValueError("Empty saved csv file.")
    
    return final_processed_data
           













    
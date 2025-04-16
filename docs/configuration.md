# Configuration
Make a copy of the config.template.json inside the root directory and name it onfig.json.
 ``` bash
cp config.template.json config.json
```
All settings are specified in the `config.json` file. Open that file in your text editor ( Visual Studio Code, TextEdit, etc.. ) and update paths and parameters inside the file to match your data and preferences. Do not change the keys in the config file. Otherwise the code crashes. Only change the values.
### Notes: 
- Do not change the keys in the config file. Otherwise the code crashes. Only change the values.
 - Folder Structure Requirement: 
Please do not modify the folder structure of the pipeline. 
The following folders must remain organized inside the data directory, which itself must be placed inside the main protein-expression-pipeline/ project folder:
protein-expression-pipeline/
├── data/                     # Input data and intermediate data
│   ├── raw/                  # Raw image stacks
│   ├── GFP/                  # GFP image stacks
│   ├── RFP/                  # RFP image stacks
│   ├── projected/            # Max projections
│   ├── mask/                 # Cellpose segmentation masks
│   └── ...           

When you set file paths in your config.json, only the first part of the path (up to the project directory) may vary depending on where the project is located on your system.

For example, the path to raw data might look like this:
/Users/your-username/Projects/protein-expression-pipeline/data/raw

Just make sure the structure after protein-expression-pipeline/ remains unchanged. This ensures the code can correctly locate all necessary files.

#### example:
##### "Path_settings"
Values: has a nested dictionary (with keys and values) to store the information about the analysis path and file names.
- Location of raw data: 
    "input_dir": "/Users/masoomeshafiee/Projects/protein-expression-pipeline/data/raw" 
- Location of GFP stacks:
    "GFP_dir": "/Users/masoomeshafiee/Projects/protein-expression-pipeline/data/GFP",
- Location of RFP stacks:
    "RFP_dir": "/Users/masoomeshafiee/Projects/protein-expression-pipeline/data/RFP",
- Location of projected images:
    "projected_dir": "/Users/masoomeshafiee/Projects/protein-expression-pipeline/data/projected",
- Location of masks after cellpose segmentation:
    "mask_dir": "/Users/masoomeshafiee/Projects/protein-expression-pipeline/data/mask",
- Location of saved outputs:
    "output_dir":"/Users/masoomeshafiee/Projects/protein-expression-pipeline/output",
- Name of output file (you can change it)
    "output_name":"processed_data.csv",

- Suffixes to be added at the end of filenames after each step of analysis (You can change them.)
    "GFP_suffix" : "_GFP.TIF",
    "RFP_suffix" : "_RFP.TIF",
    "projection_suffix":"_GFP_projection.TIF",
    "mask_suffix": "_GFP_projection_cp_masks.png",
- name of protein and condition (untreated, UV light, etc.)
    "protein_name": "Rfa1",
    "condition": "untreated"

##### "active_slice_settings"
Settings related to identifying the active slices (the images within the stack that the cell is acutually in them):
- "plot_intensity_profile": (ture or false)
    - true: if you want to plot the intensity distribution of the images in the stack for each cell.
    - false: it does not plot the intensity distribution.
- "drop_threshold": 90
The precentage of intensity drop relative to the focal plane of the cell to consider a slice as inactive or active slice (ex. if the total intensity of a slice is 90% less than the focal slice, that slice does not contain the cell and thefore is not counted for calculating the total intensity.)

##### "Analysis_settings"
- ratio of mNeonGreen intensity in the green channel over the red channel:
"rg":9.390 (standard, you can change it incase it differs.)
- ratio of mNeonGreen intensity in the red channel over the green channel:
"ra":1.137, (standard, you can change it incase it differs.)

- "single_mNG_intensity":710.90 ( standard, you can change it incase it differs.)

##### "stats_summary": (ture or false)
- if true: the pipeline performs the statistical analysis

#####  "plot_copy_number": (ture or false)
- if true: the pipeline plots the distribution of protein copy numbers 


##### "Plot_settings" 
The settings for the histogram and the distribution plots. You can change them as desired.
    "bins": 20,
    "color": "skyblue",
    "edgecolor": "black",
    "alpha": 0.7,
    "kde": false,
    "histogram_legend": "Copy number histogram",
    "fit_legend": "Normal fit",
    "title": "Copy Number Distribution",
    "title_fontsize": 16,
    "xlabel": "Copy Number",
    "x_fontsize": 14,
    "ylabel": "Frequency",
    "y_fontsize": 14,
    "add_legened": true




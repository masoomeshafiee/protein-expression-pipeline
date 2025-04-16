# Protein Expression Analysis Pipeline


A modular and reproducible image analysis pipeline to extract and quantify protein expression levels from confocal fluorescent microscopy data using Python.  
The pipeline is designed for analyzing multi-channel images (green and red channels) acquired using a dual-camera system.

For detailed explanations, module breakdowns, and pipeline diagrams, please refer to the docs/ and example/ directory.
## Features

- Preprocessing of dual-channel image stacks
- Compatible with Cellpose for segmentation
- Focal and active slice detection to robustly extract fluorescence signals
- Intermediate results saved to enhance traceability
- Cell autofluorescence correction and intensity normalization
- Single-cell copy number quantification
- Statistical summaries
- Flexible and customizable plotting
- Real-time logging to easily track errors and monitor pipeline progress
- Metadata logging for reproducibility

## Installation

This project supports:
- Python 3.9.6
- Installation via pip or conda

#### Option 1: Using Conda (Recommended)
``` bash
conda env create -f environment.yml
conda activate protein-expression-env
```
#### Option 2: Using pip
``` bash
pip install -r requirements.txt
```
## Project Structure
``` r
protein-expression-pipeline/
│
├── config.json               # Configuration file with user settings
├── environment.yml           # Conda environment file
├── requirements.txt          # Pip dependencies
├── README.md                 # Project overview and instructions
├── .gitignore                # Git ignored files
│
├── docs/                   # Extended documentation
│
├── data/                     # Input data and intermediate data
│   ├── raw/                  # Raw image stacks
│   ├── GFP/                  # GFP image stacks
│   ├── RFP/                  # RFP image stacks
│   ├── projected/            # Max projections
│   ├── mask/                 # Cellpose segmentation masks
│   └── ...                  
│
├── output/                   # Results, plots, processed CSVs, Metadata
│
└── src/                      # Source code
    ├── run_preprocess.py   # run preprocess functions
    ├── preprocess.py         # preprocess module
    ├── pipeline.py           # Main execution script
    ├── segmentation.py       # Mask loader
    ├── load_data.py          # Stack loading module
    ├── analysis.py           # Core analysis functions
    ├── plots.py              # Plotting logic
    ├── plot_only.py        # Plot only option
    ├── stats.py              # Statistics calculation
    └── save_metadata.py      # Reproducibility logger
```

## How to use
 ##### 0. Place the raw data (dual image.TIF) in the data/raw directory.
 #
 ##### 1. Configure config.json
Make a copy of the config.template.json inside the root directory and name it onfig.json.
 ``` bash
cp config.template.json config.json
```
Update paths and parameters inside the `config.json` file to match your data and preferences.
For more instruction read the docs file. 

##### 2. Navigate to the root directory and run the run_preprocess.py
- Spliting dual-camera stacks into GFP and RFP channels
- Performing max projection along the z-axis (for segmentation)
 ``` bash
python src/run_preprocess.py
```
The projected GFP images are automatically saved under data/projected directory ready for segmentation.

##### 3. Proceed with the segmentation using CellPose. 
- Perform segmentation externally using Cellpose
- Save .png mask files in the data/mask directory

##### 4. Run the full analysis pipeline
#
``` bash
python src/pipeline.py
```
The outputs will automatically be saved in the output directory. The outputs are : 
- processed_data.csv – Full copy number analysis
- copy_number_stats.csv – Summary statistics
- copy number plots as both png and svg files
- metadata_<proteinname>_<timestamp>.json – Reproducibility file (settings, versions)

##### 5. Plot without reprocessing (Optional)
#
``` bash
python src/plot_only.py
```
Use this script to try different plotting options without rerunning the analysis pipeline.

## Example Usage
In your terminal: 
1. Navigate to the root directory
2. Create and activate the protein-expression-env
3. Place your data in the Data/raw/ directory
4.Change the configuration as desired
5. Run the pipeline
```bash
cd protein-expression-pipeline
conda activate protein-expression-env
python3 run_preprocess.py
# Perform cellpose segmentation using the images in the projection directory
python3 src/pipeline.py 
python3 plot_only.py # repeat as many, change the config.json file
```

## Notes
- You can find a working example in the example/ directory with input images, intermediate results, and final outputs.
- Initially designed for budding yeast strains with mNeonGreen-tagged proteins. Easily adaptable to other organisms, such as E. coli
- Supports reproducible research via auto-saved metadata.
- Built with flexibility and ease of extension in mind.
- Designed for biomedical researchers.

## Contributors
- ###### Masoumeh Shafiei

For questions or to contribute, please contact Masoumeh Shafiei.



# Troubleshooting
This guide provides solutions to common issues encountered while running the Protein Expression Analysis Pipeline.

#### 1. Configuration & Setup
🔸 Issue: FileNotFoundError when loading config.json
   Cause: The config file is missing, renamed, or incorrectly placed.
   Fix:
   - Ensure config.json exists in the top-level project directory.
   - Use an absolute or correctly relative path to it in your script.

🔸 Issue: FileNotFoundError despite providing a path
 Fix: 
 - Make sure all paths in config.json reflect the current folder structure.
 If you moved or renamed files or folders after your last run, update config.json accordingly.



🔸 Issue: Incorrect or missing keys in config
Cause: Config keys (e.g., "Path_settings", "protein_name") are missing or misnamed.
Fix:
- Double-check the structure of config.json. Use the template provided in the documentation.
- Double-check the config keys, they should not be changed. 
- Validate JSON formatting (use jsonlint).

#### 2. Preprocessing Stage
🔸 Issue: “No image stacks were loaded. Aborting processing.”
Cause: Invalid or empty input paths.
Fix:
- Ensure your input_dir and file_name in config.json are correct.
- Verify that the .tif file exists and is readable.

#### 3. Segmentation
🔸 Issue: “Loading masks failed.” / Empty mask dictionary
Cause: No valid segmentation masks found or incorrect path.
Fix:
- Confirm that segmentation .png files exist in segmentation_dir.
- Check the naming and file extensions match what’s expected.

🔸 Issue: Loaded masks don’t match image dimensions
Cause: Mismatched segmentation size or format.
Fix:
- Ensure segmentation masks are the same shape as the image projections.

#### 4. Analysis
🔸 Issue: "No cells were segmented. Aborting processing."
Cause: The masks provided do not contain any non-zero cell labels.
Fix:
- Open the mask .png files to verify that segmentation was successful.
- Make sure the masks were generated and saved correctly (check for proper data type and nonzero values).
- Check that the filenames in your masks and image_stacks dictionaries match exactly.

🔸 Issue: "No active slices found for any cells. Aborting processing."
Fix:
- Inspect the intensity profiles by setting "plot_intensity_profile": true in the config to debug visually.

🔸 Issue: "No intensity data calculated. Aborting processing."
Cause:
- Active slices may be empty.
- The RFP/GFP stack arrays might contain only zeros (possibly due to a masking issue).

Fix:
- Make sure that segmentation is working and binary masks are correctly isolating cell regions.
- Double-check image preprocessing and intensity scaling before this step.
- make sure the keys in the config.json are not changed. 

🔸 Issue: “Processing completed successfully for 0 cells.”
Cause: Segmentation masks may be empty.
Fix:
- Ensure your segmentation masks contain valid cell labels.

🔸 Issue: "Empty saved csv file."
Cause:
Likely due to failure at one of the earlier steps—no valid data made it to the saving stage.
Fix:
- Look at earlier logs to determine which step failed.
- Use logging.DEBUG level for deeper inspection of what's missing.

🔸 Issue: FileNotFoundError during saving
Cause: The output_path directory does not exist yet.
Fix:
- Ensure that the path set under "Path_settings" in config.json exists, or create it manually before running the pipeline.

🔸 Issue: TypeError or KeyError during config or dictionary access
Cause:
A config field like "rg", "ra", or "single_mNG_intensity" may be missing.
Fix:
- Double-check that all fields in config.json are correctly spelled and present.
- Use print(config) or logging statements to debug config contents.

🔸 Issue: Empty or incorrect plots when plot_intensity_profile=True
Cause:
GFP channel might not have been loaded correctly.
The image may be mostly zeros due to masking or incorrect channel assignment.
Fix:
- Confirm that the GFP images are non-empty before segmentation.
- Visualize the image stacks and masks together to ensure alignment.

#### 5. Plotting & Statistics
🔸 Issue: “Copy Number” column missing in processed CSV
Cause: Processing did not complete or Copy Number wasn’t saved.
Fix:
- Re-run the pipeline from the start and ensure processing() outputs include the column.
- Confirm column names haven't been altered manually.

🔸 Issue: Plotting script does nothing
Cause: No data or plot config missing.
Fix:
- Make sure plot_copy_number_distribution() receives a non-empty array.
- Validate keys in Plot_settings (e.g., color, bins, etc.).

#### 6. Metadata
🔸 Issue: Metadata file not saved
Cause: Incorrect output directory or write permissions.
Fix:
- Ensure output_dir exists and is writable.
- Check for typos in config.json under Path_settings.

#### 7. Environment & Dependencies
🔸 Issue: ModuleNotFoundError
Cause: Required packages are missing.
Fix:
- Set up and activate your environment before running the pipeline
- Install dependencies using: pip install -r requirements.txt

##### Note: 
Create the environment inside the same directory where the pipeline lives to keep things organized and reproducible.

🔸 Issue: tifffile.TiffFileError or image loading errors
Cause: Corrupt or unsupported TIFF file format.
Fix:
- Open the file with another viewer to confirm it's valid.
- Re-export or convert the image using an image editor or ImageJ.

# Debugging Tips
- Use logging messages to trace the pipeline step-by-step.
- Add print() or pdb.set_trace() for in-depth inspection.
- Try running each module (e.g., run_preprocess.py) independently.

#  Still stuck?
Feel free to open an issue on GitHub with:
- The error message
- A description of what you were trying to do
- Your config.json (if not sensitive)
- Screenshot or logs

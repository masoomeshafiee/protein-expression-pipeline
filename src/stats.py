import numpy as np
from scipy import stats
import pandas as pd
import os
import logging
def compute_stats(copy_numbers, output_dir):
    """Computes and returns summary statistics for the copy numbers."""

    if len(copy_numbers) == 0:
        logging.warning("The input copy_numbers list is empty. No statistics will be computed.")
        return
    
    try:

        mean_copy_number = np.mean(copy_numbers)
        median_copy_number = np.median(copy_numbers)
        std_copy_number = np.std(copy_numbers)
        skew_copy_number = stats.skew(copy_numbers)
        kurtosis_copy_number = stats.kurtosis(copy_numbers)


    except Exception as e:
        logging.error(f"Error during computation of statistics: {e}")
        return
    
    stats_summary = {
    'Mean Copy Number': mean_copy_number,
    'Median Copy Number': median_copy_number,
    'Standard Deviation': std_copy_number,
    'Skewness': skew_copy_number,
    'Kurtosis': kurtosis_copy_number
        }
    # Create a DataFrame and save it to a CSV file
    try: 
        stats_df = pd.DataFrame([stats_summary])
        stats_df.to_csv(os.path.join(output_dir, 'copy_number_stats.csv'), index=False)
        logging.info("Summary statistics saved successfully")
    except Exception as e:
        logging.error(f"error while saving the stats to CSV:{e}")

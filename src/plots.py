import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import logging
import os


def plot_copy_number_distribution(copy_numbers, output_dir, plot_settings):

    """
    Generates and saves a plot of the copy number distribution.
    
    args:
     - copy numbers (np array): for all the cells
     - output_dir (str): directory to save the plots
     - plot_settings: (config dict): for plot setting

    
    """

    if len(copy_numbers) == 0:
        logging.warning("The input copy_numbers list is empty. Nothing was plotted.")
        return
    try:

        # Fit a normal distribution to the data
        mu, std = stats.norm.fit(copy_numbers)

        # Plot histogram and normal distribution fit
        plt.figure(figsize=(10, 6))

        sns.histplot(copy_numbers, kde=plot_settings["kde"], alpha=plot_settings['alpha'], bins=plot_settings["bins"], color=plot_settings["color"], edgecolor = plot_settings["edgecolor"], stat="density", label=plot_settings["histogram_legend"])
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2, label=plot_settings["fit_legend"])
        plt.title(plot_settings["title"], fontsize = plot_settings["title_fontsize"])
        plt.xlabel(plot_settings['xlabel'], fontsize = plot_settings["x_fontsize"])
        plt.ylabel(plot_settings["ylabel"], fontsize = plot_settings["y_fontsize"])
        if plot_settings["add_legened"]:
            plt.legend()
        
        logging.info('sucsussfully plotted the copy number')

    except Exception as e:
        logging.error(f"Error during plotting the copy number: {e}")
        return

    # Save plot 
    try:
        plot_filepath = os.path.join(output_dir, 'copy_number_distribution.png')
        plt.savefig(plot_filepath, format='png')
        #plt.close()

        svg_file_path = os.path.join(output_dir, 'copy_number_distribution.svg')
        plt.savefig(svg_file_path, format='svg')
        plt.show()
        #plt.close()

        logging.info('sucsussfully saved the plot the in the output directory')

    except Exception as e:
        logging.error(f'failed to save the plot the in the output directory: {e}')
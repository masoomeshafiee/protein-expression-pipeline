import pandas as pd
import numpy as np
import os
import logging
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.mixture import GaussianMixture
# configure logging
logging.basicConfig(level=logging.INFO)


def load_integrated_intensity(folder_path):
    """
    Loads integrated mNG intensity data from CSV files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing CSV files.
    
    Returns:
        pd.DataFrame: DataFrame containing integrated intensity data for all the images of the stacks of the different field of views. 
    """

    all_date = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            try:
                current_df = pd.read_csv(file_path)
                # add the file name as a column after the indext ( second column) to identify the source 
                current_df.insert(1, "file_name", file_name)
                all_date.append(current_df)
            except Exception as e:
                logging.error(f"Failed to load {file_name}: {e}")
                continue
    if all_date:
        integrated_intensity_df = pd.concat(all_date, ignore_index=True)
        logging.info(f"Loaded integrated intensity data with {len(integrated_intensity_df)} entries.")
        return integrated_intensity_df
    else:
        logging.error("No CSV files found or failed to load any data.")
        raise ValueError("No data loaded from CSV files.")
    
def clean_integrated_intensity_data(df, column_name="Intens"):
    """
    Cleans the integrated intensity DataFrame by removing invalid entries, such as NaN values and negative intensities.

    Args:
        df (pd.DataFrame): DataFrame containing integrated intensity data.
    
    Returns:
        pd.DataFrame: Cleaned DataFrame with valid integrated intensity entries.
    """
    initial_count = len(df)
    # Remove rows with NaN values in "Integrated Intensity" column
    df_cleaned = df.dropna(subset=[column_name])
    # Remove rows with negative values in "Integrated Intensity" column
    df_cleaned = df_cleaned[df_cleaned[column_name] >= 0]
    final_count = len(df_cleaned)
    logging.info(f"Cleaned integrated intensity data: removed {initial_count - final_count} invalid entries.")
    return df_cleaned


def clean_integrated_intensity_data_2(df, column_name="Intens",max_pct=99.5, iqr_k=3.0):
    # to numeric
    s = pd.to_numeric(df[column_name], errors="coerce")
    s = s.replace([np.inf, -np.inf], np.nan).dropna()
    s = s[s > 0]

    # log-space robust range
    logv = np.log10(s)
    q1, q3 = np.percentile(logv, [25, 75])
    iqr = q3 - q1
    lo = q1 - iqr_k * iqr
    hi = q3 + iqr_k * iqr

    # also enforce a soft upper cap (handles tiny samples with massive spikes)
    soft_hi = np.percentile(logv, max_pct)

    hi = min(hi, soft_hi)

    keep = (logv >= lo) & (logv <= hi)
    kept = s[keep]

    df_cleaned = df.loc[kept.index].copy()
    df_cleaned[column_name] = kept
    logging.info(
        f"Cleaned: {len(df)}→{len(df_cleaned)} rows | "
        f"log10 range kept ~ [{lo:.2f}, {hi:.2f}] | "
        f"median={np.median(kept):.3g}, 99%={np.percentile(kept,99):.3g}"
    )
    return df_cleaned

def fit_integrated_intensity(df, column_name="Intens"):
    """
    Fits the integrated intensity data to find the single mNG intensity using a histogram and Gaussian fitting.

    Args:
        - df (pd.DataFrame): Cleaned DataFrame containing integrated intensity data.
        - column_name (str): Name of the column with integrated intensity values.
    Returns:
        - single_mNG_intensity (float): Estimated single mNG intensity.
        - fit_params (dict): Parameters of the Gaussian mixture model fit.
        - matplotlib.figure.Figure: The histogram figure with the Gaussian mixture fit.
    """

    integrated_intensities = df[column_name].values.reshape(-1, 1)
    # Fit a Gaussian Mixture Model
    gmm = GaussianMixture(n_components=2, random_state=0)
    gmm.fit(integrated_intensities)
    means = gmm.means_.flatten()
    weights = gmm.weights_.flatten()
    # Assume the smaller mean corresponds to 16 units mean intensity
    sixteen_units_mNG_intensity = np.min(means)
    # Assume the larger mean corresponds to 32 units mean intensity
    thirty_two_units_mNG_intensity = np.max(means)
    single_mNG_intensity = sixteen_units_mNG_intensity / 16.0
    fit_params = {
        "16_units_mean": sixteen_units_mNG_intensity,
        "32_units_mean": thirty_two_units_mNG_intensity,
        "single_mNG_intensity": single_mNG_intensity,
        "16_units_weight": weights[np.argmin(means)],
        "32_units_weight": weights[np.argmax(means)]
    }
    # plot histogram alon

    # Plot histogram and GMM fit
    fig, ax = plt.subplots(figsize=(10, 6))
    counts, bins, _ = ax.hist(integrated_intensities, bins=50, density=True, alpha=0.6, color='g', label='Data Histogram')
    x = np.linspace(bins[0], bins[-1], 1000).reshape(-1, 1)
    logprob = gmm.score_samples(x)
    pdf = np.exp(logprob)
    ax.plot(x, pdf, '-k', label='GMM Fit')
    ax.set_title('Integrated mNG Intensity Histogram with GMM Fit')
    ax.set_xlabel('Integrated Intensity')
    ax.set_ylabel('Density')
    ax.legend()
    logging.info(f"Fitted single mNG intensity: {single_mNG_intensity:.2f}")
    return single_mNG_intensity, fit_params, fig

def fit_integrated_intensity_2(df, column_name="Intens", n_components=None, random_state=0):
    """
    Fit a GMM to log10(intensity). Overlay PDF on a histogram of log10 values.
    """
    vals = df[column_name].values
    logI = np.log10(vals).reshape(-1, 1)

    # Auto-select components via BIC if not specified (2–3 are typical here)
    if n_components is None:
        bics = []
        gmms = []
        for k in (1, 2, 3):
            g = GaussianMixture(n_components=k, random_state=random_state)
            g.fit(logI)
            bics.append(g.bic(logI))
            gmms.append(g)
        gmm = gmms[int(np.argmin(bics))]
    else:
        gmm = GaussianMixture(n_components=n_components, random_state=random_state).fit(logI)

    means_log = gmm.means_.flatten()               # in log10 space
    weights = gmm.weights_.flatten()
    order = np.argsort(means_log)
    means_log = means_log[order]
    weights = weights[order]

    # Back-transform to linear for reporting
    means_linear = 10 ** means_log

    # Your 16/32 mapping (if indeed correct for this dataset)
    sixteen_units_mNG_intensity = means_linear[0]   # smallest mode
    thirty_two_units_mNG_intensity = means_linear[-1]
    single_mNG_intensity = sixteen_units_mNG_intensity / 16.0

    fit_params = {
        "gmm_components": int(gmm.n_components),
        "means_log10": means_log.tolist(),
        "means_linear": means_linear.tolist(),
        "weights": weights.tolist(),
        "16_units_mean_linear": float(sixteen_units_mNG_intensity),
        "32_units_mean_linear": float(thirty_two_units_mNG_intensity),
        "single_mNG_intensity_est": float(single_mNG_intensity),
    }

    # Plot: histogram of log10 values + GMM PDF (in log space)
    fig, ax = plt.subplots(figsize=(10, 6))
    counts, bins, _ = ax.hist(logI.ravel(), bins=30, density=True, alpha=0.6, label="Data (log10)")
    x_log = np.linspace(bins[0], bins[-1], 100).reshape(-1, 1)
    pdf_log = np.exp(gmm.score_samples(x_log))     # density in log space
    ax.plot(x_log, pdf_log, "-k", label="GMM fit")
    ax.set_title("Integrated mNG Intensity (log10) with GMM Fit")
    ax.set_xlabel("log10(Integrated Intensity)")
    ax.set_ylabel("Density")
    ax.legend()

    logging.info(f"GMM on log10 intensities | K={gmm.n_components} | means_log10={means_log} | weights={weights}")
    logging.info(f"Estimated single mNG intensity (linear units): {single_mNG_intensity:.3g}")
    return single_mNG_intensity, fit_params, fig

def get_single_mNG_intensity(get_single_mNG_intensity):
    """
    Main function to get single mNG intensity from integrated intensity data.

    Args:
        get_single_mNG_intensity (dict): Configuration dictionary with keys:
            - data_path (str): Path to the folder containing integrated intensity CSV files.
            - column_name (str): Name of the column with integrated intensity values.
            - output_dir (str): Directory to save output plots.
    
    Returns:
        float: Estimated single mNG intensity.
    """
    data_path = get_single_mNG_intensity["data_path"]
    column_name = get_single_mNG_intensity["column_name"]
    output_dir = get_single_mNG_intensity["output_dir"]

    # Load integrated intensity data
    integrated_intensity_df = load_integrated_intensity(data_path)

    # Clean the data
    cleaned_df = clean_integrated_intensity_data(integrated_intensity_df, column_name=column_name)

    # Fit the data to find single mNG intensity
    single_mNG_intensity, fit_params, fig = fit_integrated_intensity_2(cleaned_df, column_name=column_name, n_components=1, random_state=0)


    # Save the plot
    plot_path = os.path.join(output_dir, "integrated_mNG_intensity_fit.png")
    fig.savefig(plot_path)
    logging.info(f"Saved integrated intensity fit plot to: {plot_path}")

    # save fit parameters to a csv file
    fit_params_path =  os.path.join(output_dir, "integrated_mNG_intensity_fit_params.csv")
    fit_params_df = pd.DataFrame([fit_params])
    fit_params_df.to_csv(fit_params_path, index=False)
    logging.info(f"Saved fit parameters to: {fit_params_path}")

    # save the cleaned data to a csv file
    cleaned_data_path = os.path.join(output_dir, "cleaned_integrated_mNG_intensity_data.csv")
    cleaned_df.to_csv(cleaned_data_path, index=False)
    logging.info(f"Saved cleaned integrated intensity data to: {cleaned_data_path}")

    print(cleaned_df["Intens"].describe(percentiles=[.01,.1,.5,.9,.99]))

    return single_mNG_intensity



conf=  {"data_path": "/Users/masoomeshafiee/Downloads/Results_1_20251007_Nup59_mNG_25_laser",
  "column_name": "Intens",
  "output_dir": "/Users/masoomeshafiee/Downloads/Results_1_20251007_Nup59_mNG_25_laser/integrated_intensity_result"}

single_mNG_intensity = get_single_mNG_intensity(conf)

print(f"Estimated single mNG intensity: {single_mNG_intensity:.2f}")
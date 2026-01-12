import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from .load import extract_pixel_columns


def estimate_baseline(y):
    baseline = np.minimum.accumulate(y)
    return baseline


def clean_subframe(row_df):
    if len(row_df) != 1:
        raise ValueError("clean_subframe expects exactly one row")

    pix_cols = extract_pixel_columns(row_df)
    intensity = row_df[pix_cols].iloc[0].astype(float).values
    pixel = np.arange(len(intensity))

    baseline = estimate_baseline(intensity)
    corrected = intensity - baseline
    smoothed = savgol_filter(corrected, 11, 3)
    normalized = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min() + 1e-9)

    return pd.DataFrame({
        "Pixel": pixel,
        "Normalized": normalized,
        "Smoothed": smoothed
    })

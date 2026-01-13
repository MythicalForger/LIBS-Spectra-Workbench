import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from .load import extract_pixel_columns
from scipy import sparse
from scipy.sparse.linalg import spsolve

def estimate_baseline_asls(y, lam=1e5, p=0.01, n_iter=10):
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L-2))
    w = np.ones(L)

    for _ in range(n_iter):
        W = sparse.diags(w, 0)
        Z = W + lam * D @ D.T
        baseline = spsolve(Z, w * y)
        w = p * (y > baseline) + (1 - p) * (y < baseline)

    return baseline


def clean_subframe(row_df):
    if len(row_df) != 1:
        raise ValueError("clean_subframe expects exactly one row")

    pix_cols = extract_pixel_columns(row_df)
    intensity = row_df[pix_cols].iloc[0].astype(float).values
    pixel = np.arange(len(intensity))

    baseline = estimate_baseline_asls(intensity)
    corrected = intensity - baseline
    smoothed = savgol_filter(corrected, 11, 3)
    normalized = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min() + 1e-9)

    return pd.DataFrame({
        "Pixel": pixel,
        "Normalized": normalized,
        "Smoothed": smoothed
    })

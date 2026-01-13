import numpy as np
import pandas as pd


def combine_subframes(
    cleaned_subframes,
    persistence_df,
    shot_id,
    pixel_tol=3,
    min_subframes=2
):
    persistent = persistence_df[persistence_df["shot_id"] == shot_id]

    if persistent.empty:
        print( "No persistent peaks found in ", persistence_df["shot_id"])
        return None

    persistent_pixels = persistent["mean_pixel"].values

    # Stack intensities
    all_pixels = cleaned_subframes[0]["Pixel"].values
    stack = np.stack(
        [df["Normalized"].values for df in cleaned_subframes],
        axis=0
    )

    combined = np.zeros_like(all_pixels, dtype=float)
    mask = np.zeros_like(all_pixels, dtype=bool)

    for p in persistent_pixels:
        close = np.abs(all_pixels - p) <= pixel_tol
        mask |= close

    # Median combine only persistent regions
    combined[mask] = np.median(stack[:, mask], axis=0)

    # Outside persistent regions → weak median background
    combined[~mask] = np.median(stack[:, ~mask], axis=0)

    return pd.DataFrame({
        "Pixel": all_pixels,
        "Combined_Normalized": combined
    })

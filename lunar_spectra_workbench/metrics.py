import pandas as pd

def peak_metrics(peaks_df, pixel_range=None):
    """
    Compute simple metrics for detected peaks.
    """

    metrics = {}

    metrics["total_peaks"] = len(peaks_df)

    if pixel_range is not None:
        pmin, pmax = pixel_range
        span = pmax - pmin
        metrics["peaks_per_1000_pixels"] = (
            len(peaks_df) / span * 1000
        )
    else:
        metrics["peaks_per_1000_pixels"] = None

    metrics["mean_prominence"] = peaks_df["Prominence"].mean()
    metrics["median_prominence"] = peaks_df["Prominence"].median()

    metrics["mean_width"] = peaks_df["Width"].mean()
    metrics["median_width"] = peaks_df["Width"].median()

    return pd.Series(metrics)

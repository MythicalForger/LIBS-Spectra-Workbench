import pandas as pd
from scipy.signal import find_peaks


def detect_peaks(
    cleaned_df,
    min_height=0.15,
    min_prominence=0.05,
    min_width=2,
    max_width=15,
    valid_pixel_range=(50, 1950)
):
    x = cleaned_df["Pixel"].values
    y = cleaned_df["Normalized"].values

    pmin, pmax = valid_pixel_range
    mask = (x >= pmin) & (x <= pmax)
    x_use, y_use = x[mask], y[mask]

    peaks, props = find_peaks(
        y_use,
        height=min_height,
        prominence=min_prominence,
        width=min_width
    )

    df = pd.DataFrame({
        "Pixel": x_use[peaks],
        "Height": props["peak_heights"],
        "Prominence": props["prominences"],
        "Width": props["widths"]
    })

    return df[df["Width"] <= max_width].reset_index(drop=True)

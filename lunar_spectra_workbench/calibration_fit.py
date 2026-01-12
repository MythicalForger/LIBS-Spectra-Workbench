import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def select_calibration_points(
    matches_df,
    min_confidence=0.3,
    min_prominence=0.08
):
    """
    Select reliable peak-line pairs for calibration.
    """

    mask = (
        (matches_df["Confidence"] >= min_confidence) &
        (matches_df["Prominence"] >= min_prominence)
    )

    calib = matches_df[mask]

    return calib[
    ["Pixel", "Ref_wavelength_nm", "Element", "shot_id", "subframe_index"]]



def fit_linear_calibration(calib_df):
    """
    Fit wavelength = a * pixel + b
    """

    X = calib_df["Pixel"].values.reshape(-1, 1)
    y = calib_df["Ref_wavelength_nm"].values


    model = LinearRegression()
    model.fit(X, y)

    a = model.coef_[0]
    b = model.intercept_

    # Residuals
    y_pred = model.predict(X)
    residuals = y - y_pred

    stats = {
        "a": a,
        "b": b,
        "rmse_nm": np.sqrt(np.mean(residuals**2)),
        "max_error_nm": np.max(np.abs(residuals)),
        "num_points": len(calib_df)
    }

    return model, stats


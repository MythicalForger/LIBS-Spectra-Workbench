import pandas as pd

from .load import find_l0_csvs, load_l0_csv, get_shot_id
from .clean import clean_subframe
from .peaks import detect_peaks
from .match import match_elements
from .calibration_fit import select_calibration_points, fit_linear_calibration


class AnalysisResult:
    def __init__(self, matches, calibration):
        self.matches = matches
        self.calibration = calibration


def analyze_day(day_dir):
    all_matches = []

    csv_files = find_l0_csvs(day_dir)

    # --- first pass: collect provisional matches ---
    for csv in csv_files:
        df = load_l0_csv(csv)
        shot_id = get_shot_id(csv)

        for idx, row in df.iterrows():
            cleaned = clean_subframe(row.to_frame().T)
            peaks = detect_peaks(cleaned)

            if peaks.empty:
                continue

            # provisional calibration (rough)
            matches = match_elements(
                peaks,
                shot_id=shot_id,
                subframe_index=idx,
                calib=(0.25, 200.0),
                tolerance_nm=1.0
            )

            if not matches.empty:
                all_matches.append(matches)

    all_matches_df = pd.concat(all_matches, ignore_index=True)

    # --- calibration per day ---
    calib_pts = select_calibration_points(all_matches_df)
    _, calib_stats = fit_linear_calibration(calib_pts)

    return AnalysisResult(all_matches_df, calib_stats)

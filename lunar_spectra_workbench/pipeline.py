import pandas as pd
from .load import find_l0_csvs, load_l0_csv, get_shot_id
from .clean import clean_subframe
from .peaks import detect_peaks
from .match import match_elements
from .calibration_fit import select_calibration_points, fit_linear_calibration, fit_weighted_calibration
from .consistency import peak_persistence, subframe_quality, shot_quality
from .combine import combine_subframes


class AnalysisResult:
    def __init__(
        self,
        matches,
        calibration,
        persistence,
        subframes,
        shots,
        combined_spectra
    ):
        self.matches = matches
        self.calibration = calibration
        self.peak_persistence = persistence
        self.subframe_quality = subframes
        self.shot_quality = shots
        self.combined_spectra = combined_spectra



def analyze_day(day_dir):
    all_matches = []

    csv_files = find_l0_csvs(day_dir)
    shot_cleaned = {}
    # --- first pass: collect provisional matches ---
    for csv in csv_files:
        df = load_l0_csv(csv)
        shot_id = get_shot_id(csv)
        shot_cleaned.setdefault(shot_id, [])
        for idx, row in df.iterrows():
            cleaned = clean_subframe(row.to_frame().T)
            shot_cleaned[shot_id].append(cleaned)
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
    if not all_matches:
        raise RuntimeError("No spectral matches found for this day.")


    persistence = peak_persistence(all_matches_df)
    subframes = subframe_quality(all_matches_df, persistence)
    shots = shot_quality(subframes)

    # --- calibration per day ---
    calib_pts = select_calibration_points(all_matches_df)
    _, calib_stats = fit_weighted_calibration(calib_pts, shots)

    combined_spectra = {}

    for shot_id, frames in shot_cleaned.items():
        combined = combine_subframes(
            frames,
            persistence,
            shot_id
        )
        if combined is not None:
            combined_spectra[shot_id] = combined

    return AnalysisResult(
        all_matches_df,
        calib_stats,
        persistence,
        subframes,
        shots,
        combined_spectra
    )




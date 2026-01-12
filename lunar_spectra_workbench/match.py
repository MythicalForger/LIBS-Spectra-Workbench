import pandas as pd
from .reference_lines import REFERENCE_LINES
from .calibration import pixel_to_wavelength


def match_elements(
    peaks_df,
    shot_id,
    subframe_index,
    calib,
    tolerance_nm
):
    records = []

    for _, p in peaks_df.iterrows():
        wl = pixel_to_wavelength(p["Pixel"], *calib)

        for element, lines in REFERENCE_LINES.items():
            for ref in lines:
                delta = abs(wl - ref)
                if delta <= tolerance_nm:
                    records.append({
                        # provenance
                        "shot_id": shot_id,
                        "subframe_index": subframe_index,

                        # peak geometry
                        "Pixel": p["Pixel"],
                        "Height": p["Height"],
                        "Prominence": p["Prominence"],
                        "Width": p["Width"],

                        # spectroscopy
                        "Wavelength_nm": wl,
                        "Ref_wavelength_nm": ref,
                        "Element": element,
                        "Delta_nm": delta,
                        "Confidence": 1 - delta / tolerance_nm
                    })

    return pd.DataFrame(records)


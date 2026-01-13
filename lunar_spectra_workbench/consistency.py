import numpy as np
import pandas as pd


def peak_persistence(
    matches_df,
    pixel_tol=3,
    min_subframes=2
):
    records = []

    for (shot_id, element), g in matches_df.groupby(["shot_id", "Element"]):
        pixels = g["Pixel"].values
        subframes = g["subframe_index"].values

        used = set()

        for i, px in enumerate(pixels):
            if i in used:
                continue

            close = np.abs(pixels - px) <= pixel_tol
            idxs = np.where(close)[0]

            if len(idxs) >= min_subframes:
                used.update(idxs)

                records.append({
                    "shot_id": shot_id,
                    "Element": element,
                    "mean_pixel": pixels[idxs].mean(),
                    "num_subframes": len(idxs)
                })

    return pd.DataFrame(records)

def subframe_quality(matches_df, persistence_df):
    persistent_keys = set(
        zip(persistence_df["shot_id"], persistence_df["Element"])
    )

    rows = []

    for (shot_id, sf), g in matches_df.groupby(["shot_id", "subframe_index"]):
        total = len(g)

        persistent = sum(
            (shot_id, el) in persistent_keys
            for el in g["Element"]
        )

        rows.append({
            "shot_id": shot_id,
            "subframe_index": sf,
            "total_peaks": total,
            "persistent_peaks": persistent,
            "persistence_ratio": persistent / total if total else 0.0
        })

    return pd.DataFrame(rows)

def shot_quality(subframe_df):
    rows = []

    for shot_id, g in subframe_df.groupby("shot_id"):
        rows.append({
            "shot_id": shot_id,
            "mean_persistence": g["persistence_ratio"].mean(),
            "min_persistence": g["persistence_ratio"].min(),
            "num_subframes": len(g)
        })

    return pd.DataFrame(rows)

from pathlib import Path
import pandas as pd


def find_l0_csvs(day_dir):
    day_dir = Path(day_dir)
    return sorted(day_dir.glob("**/*_l0.csv"))


def load_l0_csv(csv_path):
    return pd.read_csv(csv_path)


def extract_pixel_columns(df):
    pix = []
    for c in df.columns:
        try:
            int(c)
            pix.append(c)
        except ValueError:
            pass
    return sorted(pix, key=lambda x: int(x))


def get_shot_id(csv_path):
    return Path(csv_path).stem.replace("_l0", "")

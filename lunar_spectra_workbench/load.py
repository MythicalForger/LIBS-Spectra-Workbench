from pathlib import Path
import pandas as pd


def find_l0_csvs(day_dir):
    day_dir = Path(day_dir)
    return sorted(day_dir.glob("**/*_l0.csv"))


def load_l0_csv(csv_path):
    return pd.read_csv(csv_path)


def extract_pixel_columns(df):
    cols = df.columns[6:2100]
    return list(cols)


def get_shot_id(csv_path):
    return Path(csv_path).stem.replace("_l0", "")

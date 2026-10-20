import pandas as pd
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / "data" / "raw" / "gsod"

def _read_csv(file_path):
    """Reads a CSV file with data types specified"""
    return pd.read_csv(
        file_path,
        parse_dates=["DATE"],
        dtype= {"FRSHTT": str, "STATION": str}
    )


def load_station(station_id, data_dir=data_dir):
    """Load and combine every yearly CSV stored under each station folder."""
    station = str(station_id)
    station_dir = Path(data_dir) / station
    csv_files = sorted(station_dir.glob('*.csv'))
    if not csv_files:
        raise FileNotFoundError(f'No {station} CSV files found in {data_dir}')
    
    frames = [_read_csv(csv_file) for csv_file in csv_files]
    combined = pd.concat(frames, ignore_index=True)
    return combined

# Load all stations data
def load_all_stations(data_dir=data_dir):
    csv_files = sorted(Path(data_dir).glob('*/*.csv'))
    if not csv_files:
        raise FileNotFoundError(f'No CSV files found in {data_dir}')
    frames = [_read_csv(csv_file) for csv_file in csv_files]
    combined = pd.concat(frames, ignore_index=True)
    return combined

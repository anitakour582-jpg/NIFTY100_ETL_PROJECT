import pandas as pd
from pathlib import Path


def load_excel(file_path):
    """
    Load an Excel file and return a Pandas DataFrame.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path)

    print(f"File loaded successfully.")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    return df


if __name__ == "__main__":
    print("loader.py is ready.")
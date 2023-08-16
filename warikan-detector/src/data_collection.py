import pandas as pd

def load_data(filepath, encoding="SHIFT_JIS"):
    return pd.read_csv(filepath, encoding=encoding)

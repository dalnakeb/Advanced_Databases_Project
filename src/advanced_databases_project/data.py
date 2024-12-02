import pandas as pd


def load_data_csv(filepath: str) -> pd.DataFrame:
    print(f"Loading data from {filepath}..")
    data_df = pd.read_csv(filepath)
    data_df = data_df.drop(columns=["FID", "the_geom", "code", "qc_flags",
                                           "wind_speed"])
    data_df["timestamp"] = pd.to_datetime(data_df["timestamp"])
    data_df.drop_duplicates("timestamp", inplace=True)
    data_df = data_df.set_index("timestamp")
    data_df = data_df.sort_index()
    print("Data loaded successfully")
    return data_df


def save_data(filepath: str, data_df: pd.DataFrame) -> None:
    print(f"Saving data to {filepath}..")
    data_df.to_csv(filepath)
    print("Data has been saved successfully")


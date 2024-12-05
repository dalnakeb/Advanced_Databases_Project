import posixpath
import pandas as pd
from datetime import datetime
from advanced_databases_project import OUTPUT_PATH, PROMETHEUS_PATH

def load_data_csv(filepath: str) -> pd.DataFrame:
    print(f"Loading data from {filepath}..")
    data_df = pd.read_csv(filepath)
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


def save_data_openmetrics(data_df, column, filepath):
    data = "# TYPE weather gauge\n"
    data_df.reset_index(inplace=True)
    for row in data_df.iterrows():
        timestamp =  str(int(row[1]["timestamp"].timestamp()))
        value = row[1][column]
        data += "weather{freq=\"1h\"} " + str(value) + " " + str(timestamp) + "\n"
    data += "# EOF"

    with open(filepath, "w", newline="\n") as file:
        file.write(data)

    print(f"Data saved successfully to {filepath}")

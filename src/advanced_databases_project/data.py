import posixpath
import pandas as pd
import numpy as np
from advanced_databases_project import PROMETHEUS_OPENMETRICS_PATH


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


def save_data_openmetrics(data_df:pd.DataFrame, column: str, filepath: str, append=False) -> None:
    """
    Saves a data frame's column in an openMetrics format with the associated timestamps, given a filepath.
    If append is True, append data to the existing openMetrics file
    :param data_df: dataframe containing a timestamp index
    :param column: column to save
    :param filepath:
    :param append:
    :return: None
    """
    data = ""
    data_df = data_df.copy()
    if not append:
        data = "# TYPE weather gauge\n"

    data_df.reset_index(inplace=True)
    for row in data_df.iterrows():
        timestamp = str(int(row[1]["timestamp"].timestamp()))
        value = row[1][column]
        data += "weather{freq=\"1h\",temp=\"" + column + "\"} " + str(value) + " " + str(timestamp) + "\n"
    data += "# EOF"

    if not append:
        with open(filepath, "w", newline="\n") as file:
            file.write(data)
            print(f"Data saved successfully to {filepath}")
    else:
        with open(filepath, "a" ,newline="\n") as file:
            file.write(data)


def gen_openmetrics_data(data_df, params, col_name):
    for param in params:
        n = param["n"]
        N = param["N"]

        filename = f"n-{n}_N-{N}.txt"
        filepath = posixpath.join(PROMETHEUS_OPENMETRICS_PATH, filename)
        if -N * (n - 1) == 0:
            data_df2 = pd.DataFrame(data_df.iloc[-N * n:][col_name])
        else:
            data_df2 = pd.DataFrame(data_df.iloc[-N * n:-N * (n - 1)][col_name])

        save_data_openmetrics(data_df2, column=col_name, filepath=filepath)
        for i in range(1, n):
            new_col_name = col_name + str(i)
            if -N * (n - i - 1) == 0:
                data_df2.insert(i, new_col_name, np.array(data_df.iloc[-N * (n - i):][col_name]))
            else:
                data_df2.insert(i, new_col_name, np.array(data_df.iloc[-N * (n - i): -N * (n - i - 1)][col_name]))

            save_data_openmetrics(data_df2, column=new_col_name, filepath=filepath, append=True)


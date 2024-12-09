import pandas as pd

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
        timestamp =  str(int(row[1]["timestamp"].timestamp()))
        value = row[1][column]
        data += "weather{freq=\"1h\", temp=\"" + column + "\"} " + str(value) + " " + str(timestamp) + "\n"
    data += "# EOF"

    if not append:
        with open(filepath, "w", newline="\n") as file:
            file.write(data)
            print(f"Data saved successfully to {filepath}")
    else:
        with open(filepath, "a" ,newline="\n") as file:
            file.write(data)
            print(f"Data appended successfully to {filepath}")

import pandas as pd


def interpolate_missing_values(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Interpolate missing values in a dataframe
    :param data_df:
    :return: dataframe with interpolated missing values
    """
    return data_df.interpolate()


def interpolate_missing_timestamps(data_df: pd.DataFrame, freq: str) -> pd.DataFrame:
    """
    Injects missing timestamps in a dataframe depending givien a frequency, and interpolate their missing data.
    :param data_df:
    :param freq: frequency of the desired timestamps in the dataframe
    :return: dataframe with interpolated missing timestamps
    """
    start_date = data_df.index[0]
    end_date = data_df.index[-1]
    full_timestamps_df = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq=freq))
    full_timestamps_df.columns = ["timestamp"]
    full_timestamps_df.set_index("timestamp", inplace=True)
    data_df = data_df.join(full_timestamps_df, how="outer").interpolate()

    return data_df
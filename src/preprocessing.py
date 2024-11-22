import pandas as pd


def parse_data(data_df: pd.DataFrame) -> pd.DataFrame:
    print("Preprocessing data..")
    # Missing values
    parsed_data_df = data_df.interpolate()

    # Missing timestamps
    start_date = parsed_data_df.index[0]
    end_date = parsed_data_df.index[-1]
    full_timestamps_df = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq="1h"))
    full_timestamps_df.columns = ["timestamp"]
    full_timestamps_df.set_index("timestamp", inplace=True)
    parsed_data_df = parsed_data_df.join(full_timestamps_df, how="outer").interpolate()
    print("Data has been preprocessed successfully..")
    return parsed_data_df

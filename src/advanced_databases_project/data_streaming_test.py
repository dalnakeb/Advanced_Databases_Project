from flask import Flask, Response
import pandas as pd
from datetime import datetime
import preprocessing, data

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome! Metrics are at."


@app.route("/weather_metrics")
def weather_metrics():
    data_chunk = ""
    data_chunk += "# TYPE weather gauge\n"

    global data_df
    global data_index
    global data_chunk_size

    start_index = data_index*data_chunk_size
    end_index = max((data_index+1)*data_chunk_size, data_df.shape[0])
    if start_index >= data_df.shape[0]:
        return Response("", mimetype="text/plain")

    """data_chunk_df = data_df.iloc[start_index: end_index]
    for row in data_chunk_df.iterrows():
        timestamp = str(int(datetime.fromisoformat(row[1]["timestamp"]).timestamp())*1000)
        value = str(row[1]["air_temperature"])
        data_chunk += "weather{freq=\"1h\"} " + value + " " + timestamp + "\n"
    """

    timestamp = str(int(datetime.fromisoformat(data_df.iloc[data_index]["timestamp"]).timestamp()) * 1000)
    value = str(1150 + data_index)
    print(data_df.iloc[data_index]["timestamp"])
    data_chunk += "weather{freq=\"1h\"} " + value + " " + timestamp + "\n"

    #print(data_chunk)
    data_index += 1
    return Response(data_chunk, mimetype="text/plain")


if __name__ == "__main__":
    #  data_df = data.load_csv_data(filepath="../data/aws_1hour.csv")
    #  data_df = preprocessing.parse_data(data_df)
    #  data.save_data(filepath="../data/preprocessed_aws_1hour.csv", data_df=data_df)
    data_df = pd.read_csv("../data/preprocessed_aws_1hour.csv")
    data_index = -100
    data_chunk_size = 500
    print("Streaming data..")
    weather_metrics()
    app.run(host="0.0.0.0", port=8000)

from flask import Flask, Response
import pandas as pd
from datetime import datetime
import preprocessing, data

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome! Metrics are at /stream."


@app.route('/metrics')
def metrics():
    # Format data in Prometheus text format
    metric_lines = []
    global data_counter

    if data_counter*500 >= data_df.shape[0]:
        return Response("", mimetype="text/plain")

    data_chunk_df = data_df.iloc[data_counter * 500: (data_counter+1) * 500]
    for row in data_chunk_df.iterrows():
        metric_line = ("weather_metrics{location=\"AWS_1hour\"} " + str(row[1]["air_temperature"]) +
                       " " + str(int(datetime.fromisoformat(row[1]["timestamp"]).timestamp())) + "\n")
        metric_lines.append(metric_line)

    if data_counter*500 < data_df.shape[0]:
        data_counter += 1

    return Response("".join(metric_lines), mimetype="text/plain")


if __name__ == "__main__":
  #  data_df = data.load_csv_data(filepath="../data/aws_1hour.csv")
  #  data_df = preprocessing.parse_data(data_df)
  #  data.save_data(filepath="../data/preprocessed_aws_1hour.csv", data_df=data_df)
    data_df = pd.read_csv("../data/preprocessed_aws_1hour.csv")
    data_counter = 350
    print("Streaming data..")
    app.run(host="0.0.0.0", port=8000)

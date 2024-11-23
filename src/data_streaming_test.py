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
    data_chunk_size = 1
    global temp
    temp += 2
#    timestamp1 = str(int(datetime.now().timestamp() * 1000))
 #   timestamp2 = str(int(datetime.now().timestamp() * 1000 + 1000))
    global timestamp1
    global timestamp2
    timestamp1 += 2000
    timestamp2 += 2000

    data_chunk += "weather{freq=\"1h\"} " + str(temp) + f" {timestamp1}\n"
    data_chunk += "weather{freq=\"1h\"} " + str(temp+1) + f" {timestamp2}\n"

    print(data_chunk)
    return Response(data_chunk, mimetype="text/plain")
    #return Response("", mimetype="text/plain")

"""@app.route('/weather_metrics')
def streaming_weather_data():
    metric_lines = []
    data_chunk_size = 500
    global data_counter
    global data_sent

    if data_sent:
        return Response("", mimetype="text/plain")

    if data_counter*data_chunk_size >= data_df.shape[0]:
        data_chunk_df = data_df.iloc[(data_counter-1) * data_chunk_size:]
        metric_lines.append("# HELP weather Temperature data from AWS service\n")
        metric_lines.append("# TYPE weather gauge\n")
        for row in data_chunk_df.iterrows():
            metric_line = ("weather{freq=\"AWS_1hour\"} " + str(row[1]["air_temperature"]) + " " +
                           str(int(datetime.fromisoformat(row[1]["timestamp"]).timestamp())) + "\n")
            metric_lines.append(metric_line)
            data_sent = True
        return Response("".join(metric_lines), mimetype="text/plain")

    data_chunk_df = data_df.iloc[data_counter * data_chunk_size: (data_counter+1) * data_chunk_size]
    metric_lines.append("# HELP weather Temperature data from AWS service\n")
    metric_lines.append("# TYPE weather gauge\n")
    for row in data_chunk_df.iterrows():
        metric_line = ("weather{freq=\"AWS_1hour\"} " + str(row[1]["air_temperature"]) + " " +
                       str(int(datetime.fromisoformat(row[1]["timestamp"]).timestamp())) + "\n")
        print(row)
        metric_lines.append(metric_line)

    if data_counter*data_chunk_size < data_df.shape[0]:
        data_counter += 1
    print(metric_lines[2][2])
    return Response("".join(metric_lines), mimetype="text/plain")"""


if __name__ == "__main__":
  #  data_df = data.load_csv_data(filepath="../data/aws_1hour.csv")
  #  data_df = preprocessing.parse_data(data_df)
  #  data.save_data(filepath="../data/preprocessed_aws_1hour.csv", data_df=data_df)
    data_df = pd.read_csv("../data/preprocessed_aws_1hour.csv")
  #  data_counter = 350
  #  data_sent = False
    print("Streaming data..")
    #streaming_weather_data()
    data_index = 0
    temp = 9
    timestamp1 = 1732386507000 - 120000
    timestamp2 = timestamp1 + 1000
    app.run(host="0.0.0.0", port=8000)

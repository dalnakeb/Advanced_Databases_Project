import posixpath

from flask import Flask, Response
import pandas as pd
from datetime import datetime
from advanced_databases_project import preprocessing, data, OUTPUT_PATH, PROJECT_PATH

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome! Metrics are at."


@app.route("/weather_metrics")
def weather_metrics():
    return Response("", mimetype="text/plain")


if __name__ == "__main__":
    #  data_df = data.load_csv_data(filepath="../data/aws_1hour.csv")
    #  data_df = preprocessing.parse_data(data_df)
    #  data.save_data(filepath="../data/preprocessed_aws_1hour.csv", data_df=data_df)
    #filename = "preprocessed_aws_1hour.csv"
    #filepath = posixpath.join(OUTPUT_PATH, filename)
    #data_df = pd.read_csv(filepath)
    print("Streaming data..")
    app.run(host="0.0.0.0", port=8000)

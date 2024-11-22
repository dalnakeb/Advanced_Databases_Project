import pandas as pd
from flask import Flask, Response

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome!"


@app.route('/metrics_ingestion_rate')
def metrics_ingestion_rate():
    data_size = 0
    success_rate_threshold = 0.6
    pass


@app.route('/metrics_query_latency')
def metrics_query_latency():
    query = ""
    pass


@app.route('/metrics_storage_efficiency')
def metrics_storage_efficiency():
    dataset_size = 0
    retention_period = 0
    pass


@app.route('/metrics_high_cardinality')
def metrics_high_cardinality():
    num_labels = 0
    query = ""
    pass


if __name__ == "__main__":
    data_df = pd.read_csv("../data/preprocessed_aws_1hour.csv")
    print("Starting benchmarking..")
    app.run(host="0.0.0.0", port=8000)

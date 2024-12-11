import os

import pandas as pd
import numpy as np
import subprocess
import posixpath
from advanced_databases_project import data, ingestion_speed, data_size, query_latency, prometheus, OUTPUT_PATH, PROMETHEUS_PATH, \
    PROMETHEUS_OPENMETRICS_PATH


def gen_params():
    ns = [1, 5, 10, 20, 50, 100]
    Ns = [10, 50, 100, 500, 1000, 5000, 10000, 50000]

    params = []
    for n in ns:
        for N in Ns:
            if N // n >= 10:
                param = {"n": n, "N": N // n}
                params.append(param)

    return params


if __name__ == "__main__":
    #filename = "preprocessed_aws_1hour.csv"
    #filepath = posixpath.join(OUTPUT_PATH, filename)
    #data_df = data.load_data_csv(filepath=filepath)
    #params = gen_params()
    #data.gen_openmetrics_data(data_df, params=params, col_name="air_temperature")

    #params = [{'n': 1, 'N': 10}, {'n': 1, 'N': 50}, {'n': 1, 'N': 100}, {'n': 1, 'N': 500}, {'n': 1, 'N': 1000}]
    #Bs = ["10h", "20h", "40h", "80h", "160h", "320h", "640h"]
    #ingestion_speed.plot_ingestion_speed(params=params, Bs=Bs)

    #params = [{'n': 1, 'N': 10}, {'n': 1, 'N': 50}, {'n': 1, 'N': 100}, {'n': 1, 'N': 500}, {'n': 1, 'N': 1000}]
    #Bs = ["10h", "20h", "40h", "80h", "160h", "380h", "760h"]
    #data_size.plot_data_size(params=params, Bs=Bs)

    n = 1
    N = 50000
    filename = f"n-{n}_N-{N}.txt"
    B = "320h"
    dir_name = f"{PROMETHEUS_PATH}/data_blocks"
    query_latency.ingest_data(filename=filename, B=B, dir_name=dir_name)
    rep = 100
    prometheus.run_prometheus_server(dir_name)
    query = "avg_over_time(weather[2400d] @ 1732028400)"
    query_latency = query_latency.compute_query_latency(query=query, rep=rep) // 1000000
    print(f"query_latency: {query_latency:.2f} ms")
    prometheus.stop_prometheus()


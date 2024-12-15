import os

import pandas as pd
import numpy as np
import subprocess
import posixpath
from advanced_databases_project import data, ingestion_speed, data_size, query_latency, prometheus, OUTPUT_PATH, PROMETHEUS_PATH, \
    PROMETHEUS_OPENMETRICS_PATH


def gen_params():
    ns = [1]
    Ns = [10, 100, 1000, 10000, 100000, 1000000]

    params = []
    for n in ns:
        for N in Ns:
            if N // n >= 10:
                param = {"n": n, "N": N // n}
                params.append(param)

    return params


if __name__ == "__main__":
    # Generate openMetrics data
    """filename = "preprocessed_aws_1hour.csv"
    filepath = posixpath.join(OUTPUT_PATH, filename)
    data_df = data.load_data_csv(filepath=filepath)
    params = gen_params()
    data.gen_openmetrics_data(data_df, params=params, col_name="air_temperature")"""

    #B = 1000
    #Bs = [f"{B}m", f"{B*2}m", f"{B * 4}m", f"{B * 10}m", f"{B * 30}m", f"{B * 100}m"]

    #Ingestion Speed
    #params = [{'n': 1, 'N': 10}, {'n': 1, 'N': 100}, {'n': 1, 'N': 1000}, {'n': 1, 'N': 10000}, {'n': 1, 'N': 100000}]
    #rep = 1
    #ingestion_speed.plot_ingestion_speed(params=params, Bs=Bs, rep=rep)

    # Data Size
    """params = [{'n': 1, 'N': 10}, {'n': 1, 'N': 100}, {'n': 1, 'N': 1000}, {'n': 1, 'N': 10000}, {'n': 1, 'N': 100000}]
    data_size.plot_data_size(params=params, Bs=Bs)"""

    # Ingest data
    n = 1
    N = 1000000
    B = 10000
    filename = f"n-{n}_N-{N}.txt"
   # Bs = [f"{B * 1}m", f"{B * 3}m", f"{B * 10}m", f"{B * 50}m", f"{B * 100}m"]
    dir_names = [f"{PROMETHEUS_PATH}/data_blocks_B-" + str(B) for B in Bs]

#    for dir_name, B in zip(dir_names, Bs):
 #       query_latency.ingest_data(filename=filename, B=B, dir_name=dir_name)

    # Selection query
#    rep = 20
 #   query_latency.plot_selection_latency(dir_names=dir_names, Bs=Bs, rep=rep)

    # Aggregation query
    rep = 100
    query_latency.plot_aggregation_latency(dir_names=dir_names, Bs=Bs, rep=rep)


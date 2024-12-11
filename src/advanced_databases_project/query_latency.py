import posixpath
import shutil
import subprocess
import time

import numpy as np
import requests
import matplotlib.pyplot as plt
from advanced_databases_project import PROMETHEUS_URL, PROMETHEUS_PATH, PROMETHEUS_OPENMETRICS_PATH


def compute_query_latency(query, rep):
    query_latencies = np.zeros(rep)
    for i in range(rep):
        url = f"{PROMETHEUS_URL}/api/v1/query"
        params = {"query": query}
        start_time = time.time_ns()
        response = requests.get(url, params=params)
        end_time = time.time_ns()
        query_latencies[i] = end_time - start_time

        if response.status_code != 200:
            raise Exception(response.text)
    print(response.text)
    query_latency = query_latencies.sum()
    return query_latency


def ingest_data(filename: str, B: str, dir_name):
    filepath = posixpath.join(PROMETHEUS_OPENMETRICS_PATH, filename)
    promtool_path = posixpath.join(PROMETHEUS_PATH, "promtool")
    command = [
        promtool_path,
        "tsdb",
        "create-blocks-from",
        "openmetrics",
        filepath,
        dir_name,
        "--max-block-duration=" + B,
    ]

    try:
        shutil.rmtree(dir_name)
    except:
        pass

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing the command.")
        print(e.stderr)


def plot_query_latency(query, rep):
    pass


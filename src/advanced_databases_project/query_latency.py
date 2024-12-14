import posixpath
import shutil
import subprocess
import time

import numpy as np
import requests
import matplotlib.pyplot as plt
from advanced_databases_project import prometheus, PROMETHEUS_URL, PROMETHEUS_PATH, PROMETHEUS_OPENMETRICS_PATH


def compute_query_latency(query, rep, output_text):
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
    if output_text:
        print(response.text)
    query_latency = query_latencies.mean()
    return query_latency


def ingest_data(filename: str, B: str, dir_name, delete_existent=False):
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
    if delete_existent:
        try:
            shutil.rmtree(dir_name)
        except:
            pass

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing the command.")
        print(e.stderr)


def plot_selection_latency(dir_names, Bs, rep, output_text=False):
    time_periods = [1, 10, 100, 1000, 10000, 100000, 1000000]
    query_latencies = []
    for dir_name, B in zip(dir_names, Bs):
        prometheus.run_prometheus_server(dir_name)
        query_latencies.append({"B": B, "ql": []})
        for time_period in time_periods:
            query = f"weather[{time_period}m] @ end()"
            query_latency = compute_query_latency(query=query, rep=rep, output_text=output_text) / 1000000
            query_latencies[-1]["ql"].append(query_latency)
            print(f"B:{B} - query_latency: {query_latency:.2f} ms - time period: {time_period}")
        prometheus.stop_prometheus()

    for B, query_latency in zip(Bs, query_latencies):
        plt.plot(time_periods, query_latency["ql"], label=B)
    plt.xlabel("Time Period (m)")
    plt.ylabel("Query Latency (ms)")
    plt.title("Selection Query Latency")
    plt.legend()
    plt.show()


def plot_aggregation_latency(dir_names, Bs, rep, output_text=False):
    time_periods = [1, 10, 100, 1000, 10000, 100000, 1000000]
    query_latencies = []
    for dir_name, B in zip(dir_names, Bs):
        prometheus.run_prometheus_server(dir_name)
        query_latencies.append({"B": B, "ql": []})
        for time_period in time_periods:
            query = f"avg_over_time(weather[{time_period}m])"
            query_latency = compute_query_latency(query=query, rep=rep, output_text=output_text) / 1000000
            query_latencies[-1]["ql"].append(query_latency)
            print(f"B:{B} - query_latency: {query_latency:.2f} ms - time period: {time_period}")
        prometheus.stop_prometheus()

    for B, query_latency in zip(Bs, query_latencies):
        plt.plot(time_periods, query_latency["ql"], label=B)
    plt.xlabel("Time Period (m)")
    plt.ylabel("Query Latency (ms)")
    plt.title("Aggregation Query Latency")
    plt.legend()
    plt.show()

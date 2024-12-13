import posixpath
import shutil
import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt
from advanced_databases_project import PROMETHEUS_PATH, PROMETHEUS_OPENMETRICS_PATH


def compute_ingestion_speed(filename: str, B: str, dir_name):
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
        start_time = time.time_ns()
        subprocess.run(command, check=True)
        end_time = time.time_ns()
    except subprocess.CalledProcessError as e:
        print("Error executing the command.")
        print(e.stderr)

    execution_time = (end_time - start_time) // 1000000000
    print(f"Execution Time: {execution_time:.2f} s")
    shutil.rmtree(dir_name)
    return execution_time


def plot_ingestion_speed(params, Bs, rep):
    ingestion_speeds = {}

    for B in Bs:
        Ns = []
        ingestion_speeds[B] = []
        for param in params:
            n = param["n"]
            N = param["N"]
            Ns.append(N)
            filename = f"n-{n}_N-{N}.txt"

            speeds = []
            for _ in range(rep):
                speed = compute_ingestion_speed(filename=filename, B=B, dir_name=B)
                speeds.append(speed)
            avg_speed = np.mean(speeds)

            ingestion_speeds[B].append(avg_speed)

    for B in Bs:
        plt.plot(Ns, ingestion_speeds[B], label=B)

    plt.xlabel('N')
    plt.ylabel('ingestion_speed (s)')
    plt.legend()

    plt.show()

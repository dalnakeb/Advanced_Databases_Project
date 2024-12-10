import os
import shutil
import pandas as pd
import time
import numpy as np
import subprocess
import posixpath
from advanced_databases_project import data, OUTPUT_PATH, PROMETHEUS_PATH, PROMETHEUS_OPENMETRICS_PATH
import matplotlib.pyplot as plt


def save_data_openmetrics(data_df:pd.DataFrame, column: str, filepath: str, append=False) -> None:
    """
    Saves a data frame's column in an openMetrics format with the associated timestamps, given a filepath.
    If append is True, append data to the existing openMetrics file
    :param data_df: dataframe containing a timestamp index
    :param column: column to save
    :param filepath:
    :param append:
    :return: None
    """
    data = ""
    data_df = data_df.copy()
    if not append:
        data = "# TYPE weather gauge\n"

    data_df.reset_index(inplace=True)
    for row in data_df.iterrows():
        timestamp =  str(int(row[1]["timestamp"].timestamp()))
        value = row[1][column]
        data += "weather{freq=\"1h\",temp=\"" + column + "\"} " + str(value) + " " + str(timestamp) + "\n"
    data += "# EOF"

    if not append:
        with open(filepath, "w", newline="\n") as file:
            file.write(data)
            print(f"Data saved successfully to {filepath}")
    else:
        with open(filepath, "a" ,newline="\n") as file:
            file.write(data)


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


def gen_openmetrics_data(data_df, params, col_name):
    for param in params:
        n = param["n"]
        N = param["N"]

        filename = f"n-{n}_N-{N}.txt"
        filepath = posixpath.join(PROMETHEUS_OPENMETRICS_PATH, filename)
        if -N * (n - 1) == 0:
            data_df2 = pd.DataFrame(data_df.iloc[-N * n:][col_name])
        else:
            data_df2 = pd.DataFrame(data_df.iloc[-N * n:-N * (n - 1)][col_name])

        save_data_openmetrics(data_df2, column=col_name, filepath=filepath)
        for i in range(1, n):
            new_col_name = col_name + str(i)
            if -N * (n - i - 1) == 0:
                data_df2.insert(i, new_col_name, np.array(data_df.iloc[-N * (n - i):][col_name]))
            else:
                data_df2.insert(i, new_col_name, np.array(data_df.iloc[-N * (n - i): -N * (n - i - 1)][col_name]))

            save_data_openmetrics(data_df2, column=new_col_name, filepath=filepath, append=True)

    return params


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


def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            # Add the file size, ignoring errors for inaccessible files
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                pass
    return total_size


def compute_data_size(filename, B, dir_name):
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

    dir_size = get_directory_size(directory=dir_name) // 1024
    print(f"Data Size: {dir_size:.2f} Kb")
    shutil.rmtree(dir_name)
    return dir_size


def plot_ingestion_speed(params, Bs):
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
            for _ in range(5):
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


def plot_data_size(params, Bs):
    data_size = {}
    for B in Bs:
        Ns = []
        data_size[B] = []
        for param in params:
            n = param["n"]
            N = param["N"]
            Ns.append(N)
            filename = f"n-{n}_N-{N}.txt"
            data_size[B].append(compute_data_size(filename=filename, B=B, dir_name=B))

    for B in Bs:
        plt.plot(Ns, data_size[B], label=B)

    plt.xlabel('N')
    plt.ylabel('Data_Size (Kb)')
    plt.legend()

    plt.show()


if __name__ == "__main__":
    #filename = "preprocessed_aws_1hour.csv"
    #filepath = posixpath.join(OUTPUT_PATH, filename)
    #data_df = data.load_data_csv(filepath=filepath)
    #gen_openmetrics_data(data_df, params=params, col_name="air_temperature")

    #params = [{'n': 1, 'N': 10}, {'n': 1, 'N': 50}, {'n': 1, 'N': 100}, {'n': 1, 'N': 500}, {'n': 1, 'N': 1000}]
    #Bs = ["10h", "20h", "40h", "80h", "160h", "320h", "640h"]
    #plot_ingestion_speed(params=params, Bs=Bs)

    params = [{'n': 1, 'N': 10}, {'n': 1, 'N': 50}, {'n': 1, 'N': 100}, {'n': 1, 'N': 500}, {'n': 1, 'N': 1000}]
    Bs = ["10h", "20h", "40h", "80h", "160h", "380h", "760h"]
    plot_data_size(params=params, Bs=Bs)
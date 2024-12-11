import posixpath
import shutil
import subprocess
import os
import matplotlib.pyplot as plt
from advanced_databases_project import PROMETHEUS_PATH, PROMETHEUS_OPENMETRICS_PATH


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
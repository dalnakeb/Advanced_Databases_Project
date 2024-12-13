import subprocess
from advanced_databases_project import PROMETHEUS_PATH


process = None

def run_prometheus_server(dir_name):
    global process
    command = [
        f"{PROMETHEUS_PATH}/prometheus",
        f"--config.file={PROMETHEUS_PATH}/prometheus.yml",
        f"--storage.tsdb.path={dir_name}",
        "--storage.tsdb.retention.time=2100d"
    ]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Prometheus started with PID: {process.pid}")


def stop_prometheus():
    global process
    if process and process.poll() is None:
        process.kill()
        process.wait()
        print("Prometheus process terminated.")
    else:
        print("No running Prometheus process to terminate.")

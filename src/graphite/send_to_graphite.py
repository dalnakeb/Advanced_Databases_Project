"""module used to send the datafile into graphite"""
import time
import matplotlib.pyplot as plt

import socket

# Configuration for Graphite
GRAPHITE_HOST = "localhost"
GRAPHITE_PORT = 2003

# this path means the code mut be executed from the root of the repository
DATA_FILE = "data/graphite_data.txt"

def send_to_graphite(data_file, host, port, max_line = 100000):
    """sends the data into graphite"""
    try:
        # Connect to Graphite
        start_time = time.time_ns()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            print(f"Connected to Graphite at {host}:{port}")
            # Open the file and send data line by line
            with open(data_file, "r", encoding="utf-8") as file:
                for i, line in enumerate(file):
                    if i >= max_line*4:
                        break
                    # Clean the line and send it
                    data = line.strip()
                    if data:
                        sock.sendall((data + "\n").encode())
            print("All data sent successfully!")
            end_time = time.time_ns()
            print(f"query latency for {max_line} lines: {(end_time-start_time)/1000000000} seconds")
            return (end_time-start_time)/1000000000
    except Exception as e:
        print(f"An error occurred: {e}")


N = [10,100,1000,10000,100000]
send_time_graphite = []

for n in N:
    send_time_graphite.append(send_to_graphite(DATA_FILE, GRAPHITE_HOST, GRAPHITE_PORT))

plt.plot(N, send_time_graphite)
plt.xlabel('Number of points')  # X-axis label
plt.ylabel('Time (s)')  # Y-axis label
plt.title('Graphite ingestion time')
plt.legend()
plt.show()
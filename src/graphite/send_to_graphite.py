"""module used to send the datafile into graphite"""
import time

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
    except Exception as e:
        print(f"An error occurred: {e}")

send_to_graphite(DATA_FILE, GRAPHITE_HOST, GRAPHITE_PORT)

send_time_graphite = [0.001009524, 0.002028783, 0.015961696, 0.104520756, 1.541455145]
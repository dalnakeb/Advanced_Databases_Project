import socket

# Configuration for Graphite
GRAPHITE_HOST = "localhost"
GRAPHITE_PORT = 2003

# this path means the code mut be executed from the root of the repository
DATA_FILE = "data/graphite_data.txt"

def send_to_graphite(data_file, host, port):
    try:
        # Connect to Graphite
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            print(f"Connected to Graphite at {host}:{port}")
            
            # Open the file and send data line by line
            with open(data_file, "r") as file:
                for line in file:
                    # Clean the line and send it
                    data = line.strip()
                    if data:
                        #print(f"Sending: {data}")
                        sock.sendall((data + "\n").encode())
            print("All data sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

send_to_graphite(DATA_FILE, GRAPHITE_HOST, GRAPHITE_PORT)

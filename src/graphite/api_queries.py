"""module providing the methods making api requests to graphite (set up for docker)"""

#!/usr/bin/python3
import time
import os
import matplotlib.pyplot as plt
import json
from urllib.parse import quote #inshallah ca passe
import requests
import sys

GRAPHITE_URL = "http://localhost/render"  # graphite render api's endpoint
METRIC = "environment.air_pressure"

#here, we only fetch 24 points (we have 1 per hour)
#we use the unix epoch format (seconds since 1/1/1970)
NB = 40000
UNTIL_TIME = "1732024800"
#FROM_TIME = f"{int(UNTIL_TIME) - 3600*NB}"

def query_graphite(metric, until_time, arg, n):
    """make a query to graphite's render api over the given metric, 
    and in the specified time range"""

    from_time = f"{int(UNTIL_TIME) - 3600*n}"
    params = {}
    if arg == 'graph':
        params = {
            "target": metric,
            "from": quote(from_time),
            "until": quote(until_time),
            "format": "png",
            "width": 800,
            "height": 600,
            "title": "Air Pressure Graph",
            "lineWidth": 2,
        }
    
    if arg == 'select':
        params = {
            "target": metric,
            "from": quote(from_time), 
            "until": quote(until_time),
            "format": "json",
        }
    if arg == 'aggregated':
        params = {
        "target": f"averageSeries({metric})",
        "from": quote(from_time),
        "until": quote(until_time),
        "format": "json",
        }
        
    try:
        start_time = time.time_ns()

        # Send the GET request to Graphite
        response = requests.get(GRAPHITE_URL, params=params, timeout=10)
        response.raise_for_status()

        end_time = time.time_ns()
        # Save the image locally
        # output_path = os.path.expanduser(f"~/Screenshots/graph{NB}.png")
        # with open(output_path, "wb") as f:
        #     f.write(response.content)

        # print(f"Time taken for the request: {(end_time - start_time) / 1_000_000_000:.2f} seconds")
        return (end_time - start_time) / 1000000000

    except requests.RequestException as e:
        print(f"Error querying Graphite: {e}")
        return None


def main():

    # print(f"Mode selected: {mode}")
    if len(sys.argv) != 2:
        print("there is a missing argument")
        sys.exit(1)

    N = [10,100,1000,10000, 20000, 30000, 42572]
    q_latency = []
    for n in N:
        q_latency.append(query_graphite(METRIC, UNTIL_TIME, sys.argv[1], n))

    plt.plot(N, q_latency)
    plt.xlabel('Number of points')  # X-axis label
    plt.ylabel('Time (s)')  # Y-axis label
    if sys.argv[1] == 'select':
        plt.title('Graphite SELECT query latency')  # Title

    if sys.argv[1] == 'aggregated':
        plt.title('Graphite Aggregate query latency')  # Title

    if sys.argv[1] == 'graph':
        plt.title('Graphite graph query latency')  # Title

    plt.show()  # Display the plot

if __name__ == "__main__":
    main()
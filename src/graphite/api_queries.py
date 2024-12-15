"""module providing the methods making api requests to graphite (set up for docker)"""

#!/usr/bin/python3
import time
import os
import matplotlib.pyplot as plt
import json
from urllib.parse import quote #inshallah ca passe
import requests

GRAPHITE_URL = "http://localhost/render"  # graphite render api's endpoint
METRIC = "environment.air_pressure"

#here, we only fetch 24 points (we have 1 per hour)
#we use the unix epoch format (seconds since 1/1/1970)
NB = 40000
UNTIL_TIME = "1732024800"
FROM_TIME = f"{int(UNTIL_TIME) - 3600*NB}"

def query_graphite(metric, from_time, until_time):
    """make a query to graphite's render api over the given metric, 
    and in the specified time range"""
    params = {
        "target": metric,
        "from": quote(from_time),
        "until": quote(until_time),
        "format": "png",  # Request the graph as a PNG image
        "width": 800,     # Graph width in pixels
        "height": 600,    # Graph height in pixels
        "title": "Air Pressure Graph",  # Title of the graph
        "lineWidth": 2,   # Thickness of the line in the graph
    }
    print(f"Querying with params: {params}")
    try:
        print(f"Fetching graph with params: {params}")
        start_time = time.time_ns()

        # Send the GET request to Graphite
        response = requests.get(GRAPHITE_URL, params=params, timeout=10)
        response.raise_for_status()

        end_time = time.time_ns()
        # Save the image locally
        output_path = os.path.expanduser(f"~/Screenshots/graph{NB}.png")
        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"Graph saved as ")
        print(f"Time taken for the request: {(end_time - start_time) / 1_000_000_000:.2f} seconds")

    except requests.RequestException as e:
        print(f"Error querying Graphite: {e}")
        return None

query_graphite(METRIC, FROM_TIME, UNTIL_TIME)
#print(query_data)

# N=[10,100,1000,10000, 20000, 30000, 42572]
# q_latency= [0.018931557, 0.022106593, 0.053436892, 0.183865365, 0.302734658, 0.439015871, 0.544481905]
# q_aggregate = [0.023532308, 0.025569139, 0.035183309, 0.133541588, 0.244488525, 0.334968708, 0.430350666]
# q_graph = [0.08, 0.09, 0.17, 0.31, 0.51, 0.69, 0.90]
# plt.plot(N, q_aggregate)
# plt.xlabel('Number of points')  # X-axis label
# plt.ylabel('Time (s)')  # Y-axis label
# plt.title('Graphite Aggregate query latency')  # Title
# plt.legend()  # Show legend
# plt.show()  # Display the plot
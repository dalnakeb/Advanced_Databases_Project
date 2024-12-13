"""module providing the methods making api requests to graphite (set up for docker)"""

#!/usr/bin/python3
import json
import requests
from urllib.parse import quote #inshallah ca passe

GRAPHITE_URL = "http://localhost/render"  # graphite render api's endpoint
METRIC = "environment.air_pressure"

#here, we only fetch 24 points (we have 1 per hour)
FROM_TIME = "2020-01-01 00:00:00"       #these can be changed to fetch different amount of points
UNTIL_TIME = "2020-02-01 00:00:00"

def query_graphite(metric, from_time, until_time):
    """make a query to graphite's render api over the given metric, 
    and in the specified time range"""
    params = {
        "target": metric,
        "from": quote(from_time),
        "until": quote(until_time),
        "format": "json",
    }

    try:
        # Send the GET request to Graphite
        response = requests.get(GRAPHITE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        print(f"Received data for metric '{metric}':")
        print(json.dumps(data, indent=2))
        return data

    except requests.RequestException as e:
        print(f"Error querying Graphite: {e}")
        return None

query_data = query_graphite(METRIC, FROM_TIME, UNTIL_TIME)
print(query_data)
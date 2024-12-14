"""module providing the methods making api requests to graphite (set up for docker)"""

#!/usr/bin/python3
import json
from urllib.parse import quote #inshallah ca passe
import requests

GRAPHITE_URL = "http://localhost/render"  # graphite render api's endpoint
METRIC = "environment.air_pressure"

#here, we only fetch 24 points (we have 1 per hour)
#we use the unix epoch format (seconds since 1/1/1970)
FROM_TIME = "1578675600"
UNTIL_TIME = "1732024800"

def query_graphite(metric, from_time, until_time):
    """make a query to graphite's render api over the given metric, 
    and in the specified time range"""
    params = {
        "target": metric,
        "from": quote(from_time),
        "until": quote(until_time),
        "format": "json",
        "noNullPoints": "true",
    }
    print(f"Querying with params: {params}")
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

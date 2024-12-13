#!/usr/bin/python3

import csv
from datetime import datetime
import os

# définition des path
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
input_file = os.path.join(base_dir, "data", "preprocessed_aws_1hour.csv")
output_file = os.path.join(base_dir, "data", "graphite_data.txt")

# Function pour convertir les timestamp en timestamp uix epoch, qui est le format attendu par graphite
def convert_to_epoch(timestamp_str):
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp())

#il reste encore a ignorer la 1e rangée
# Traduit les données en données pour graphite
with open(input_file, "r") as csv_file, open(output_file, "w") as output:
    reader = csv.DictReader(csv_file)
    for row in reader:
        timestamp = convert_to_epoch(row["timestamp"])
        output.write(f"environment.air_pressure {row['air_pressure']} {timestamp}\n")
        output.write(f"environment.air_temperature {row['air_temperature']} {timestamp}\n")
        output.write(f"environment.relative_humidity {row['relative_humidity']} {timestamp}\n")
        output.write(f"environment.precipitation {row['precipitation']} {timestamp}\n")

print(f"Data converted and saved to {output_file}")

######50000h de données
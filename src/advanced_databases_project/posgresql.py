import posixpath
import matplotlib.pyplot as plt
import numpy as np
import psycopg2
import subprocess
import os
import pandas as pd
import time
from advanced_databases_project import (data, OUTPUT_PATH, POSTGRESQL_BIN_PATH, POSTGRESQL_DATA_PATH, DB_NAME, DB_HOST,
                                        DB_PORT, DB_USER, DB_PASSWORD)


def plot_data_ingestion_latency(file_path):
    conn = connect_to_db()
    cursor = conn.cursor()
    time_periods = [10, 100, 1000, 10000, 100000]
    data_df = pd.read_csv(file_path).reset_index()
    ingestion_times = []
    cursor.execute("TRUNCATE TABLE weather_metrics;")
    conn.commit()
    for time_period in time_periods:
        data_df2 = data_df.tail(time_period)
        start_time = time.time_ns()
        for i, row in data_df2.iterrows():
            if i % 1000 == 0:
                print(row["timestamp"])
            cursor.execute("""
                INSERT INTO weather_metrics (timestamp, air_temperature)
                VALUES (%s, %s);
            """, (row['timestamp'], row['air_temperature']))
        conn.commit()
        end_time = time.time_ns()
        cursor.execute("TRUNCATE TABLE weather_metrics;")
        conn.commit()

        ingestion_times.append((end_time-start_time) / 1000000000)

    plt.plot(time_periods, [ingestion_time for ingestion_time in ingestion_times])
    plt.scatter(time_periods, [ingestion_time for ingestion_time in ingestion_times])
    plt.xlabel("Time Period (m)")
    plt.ylabel("Ingestion Time (s)")
    plt.title("POSTGRESQL Ingestion Time Latency")
    plt.show()
    cursor.close()
    conn.close()


def ingest_data(file_path):
    conn = connect_to_db()
    cursor = conn.cursor()
    data_df = pd.read_csv(file_path).reset_index()

    for i, row in data_df.iterrows():
        if i % 1000 == 0:
            print(row["timestamp"])
        cursor.execute("""
                INSERT INTO weather_metrics (timestamp, air_temperature)
                VALUES (%s, %s);
            """, (row['timestamp'], row['air_temperature']))
    conn.commit()
    cursor.close()
    conn.close()


def plot_selection_latency():
    conn = connect_to_db()
    cursor = conn.cursor()
    filename = posixpath.join(OUTPUT_PATH, "preprocessed_aws_1hour.csv")
    data_df = data.load_data_csv(filename).reset_index()
    time_periods = [1, 10, 100, 1000, 10000, 100000, 1000000]
    selection_times = []
    for time_period in time_periods:
        times = 0
        for i in range(100):
            if i % 10 == 0:
                print(i)
            timestamp = list(data_df.tail(time_period)["timestamp"])[0]
            start_time = time.time_ns()
            cursor.execute(f"""
                                    SELECT *
                                    FROM weather_metrics
                                    WHERE timestamp BETWEEN '{timestamp}' AND (select max(timestamp)
                                    from weather_metrics) ;""")
            conn.commit()
            end_time = time.time_ns()
            times += end_time - start_time

        times = np.mean(times)
        selection_times.append((times) / 1000000)

    plt.plot(time_periods, [selection_time for selection_time in selection_times])
    plt.scatter(time_periods, [selection_time for selection_time in selection_times])

    plt.xlabel("Time Period (m)")
    plt.ylabel("Selection Time (ms)")
    plt.title("POSTGRESQL Selection Time Latency")
    plt.show()
    cursor.close()
    conn.close()


def plot_aggregation_latency():
    conn = connect_to_db()
    cursor = conn.cursor()

    time_periods = [1, 10, 100, 1000, 10000, 100000, 1000000]
    aggregation_times = []
    for time_period in time_periods:
        times = 0
        for i in range(100):
            if i % 10 == 0:
                print(i)
            start_time = time.time_ns()
            cursor.execute(f"""
                        SELECT avg(air_temperature)
                        FROM weather_metrics
                        WHERE  timestamp >= (
                            SELECT MAX(timestamp) FROM weather_metrics
                        ) - INTERVAL '{time_period} hours';""")
            conn.commit()
            end_time = time.time_ns()
            times += end_time-start_time
        times = np.mean(times)
        aggregation_times.append((times) / 1000000)

    plt.plot(time_periods, [aggregation_time for aggregation_time in aggregation_times])
    plt.scatter(time_periods, [aggregation_time for aggregation_time in aggregation_times])
    plt.xlabel("Time Period (m)")
    plt.ylabel("Aggregation Time (ms)")
    plt.title("POSTGRESQL Aggregation Time Latency")
    plt.show()
    cursor.close()
    conn.close()


def connect_to_db():
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            host=DB_HOST,
                            password=DB_PASSWORD,
                            port=DB_PORT)
    return conn


def create_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS weather_metrics (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                air_temperature DOUBLE PRECISION NOT NULL
            );""")
    conn.commit()
    print("Table 'weather_metrics' created successfully.")
    cur.close()
    conn.close()


def plot_data_size(file_path):
    conn = connect_to_db()
    cursor = conn.cursor()
    time_periods = [10, 100, 1000, 10000, 100000]
    data_df = pd.read_csv(file_path).reset_index()
    data_sizes = []
    cursor.execute("TRUNCATE TABLE weather_metrics;")
    conn.commit()
    for time_period in time_periods:
        data_df2 = data_df.tail(time_period)
        for i, row in data_df2.iterrows():
            if i % 1000 == 0:
                print(row["timestamp"])
            cursor.execute("""
                    INSERT INTO weather_metrics (timestamp, air_temperature)
                    VALUES (%s, %s);
                """, (row['timestamp'], row['air_temperature']))
        conn.commit()
        cursor.execute("SELECT pg_size_pretty(pg_total_relation_size('weather_metrics'));")
        conn.commit()
        data_sizes.append(cursor.fetchone()[0])
        cursor.execute("TRUNCATE TABLE weather_metrics;")
        conn.commit()

    plt.plot(time_periods, [data_size for data_size in data_sizes])
    plt.scatter(time_periods, [data_size for data_size in data_sizes])
    plt.xlabel("Time Period (m)")
    plt.ylabel("Data Size")
    plt.title("POSTGRESQL Data Size")
    plt.show()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_table()
    filename = "preprocessed_aws_1hour.csv"
    filepath = posixpath.join(OUTPUT_PATH, filename)
    #plot_data_ingestion_latency(filepath)
    #plot_data_size(filepath)

    #ingest_data(filepath)
    #plot_selection_latency()
    plot_aggregation_latency()

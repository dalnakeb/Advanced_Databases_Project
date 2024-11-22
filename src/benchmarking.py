import data
import preprocessing


class Benchmarking:
    def __init__(self):
        data_df = data.load_csv_data(filepath="../data/aws_1hour.csv")
        data_df = preprocessing.parse_data(data_df)
        data.save_data(filepath="../data/preprocessed_aws_1hour.csv", data_df=data_df)

    def ingestion_rate(self, data_size: int, success_rate_threshold: float):
        pass

    def query_latency(self, query: str):
        pass

    def storage_efficiency(self, dataset_size, retention_period):
        pass

    def high_cardinality(self, num_labels, query):
        pass


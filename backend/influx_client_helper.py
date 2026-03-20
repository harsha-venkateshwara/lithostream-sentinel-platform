import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxManager:
    def __init__(self):
        self.url = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
        self.token = os.getenv("INFLUXDB_TOKEN", "my-super-token")
        self.org = os.getenv("INFLUXDB_ORG", "asml-org")
        self.bucket = os.getenv("INFLUXDB_BUCKET", "machine_metrics")

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_metric(self, data):
        p = (
            Point("machine")
            .tag("machine_id", data["machine_id"])
            .field("temperature", data["temperature"])
            .field("latency", data["latency"])
            .field("error_count", data["error_count"])
            .time(data["timestamp"], WritePrecision.S)
        )

        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=p
        )
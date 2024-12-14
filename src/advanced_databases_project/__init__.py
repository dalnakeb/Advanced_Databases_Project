from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent.absolute()
DATA_PATH = PROJECT_PATH / 'data'
OUTPUT_PATH = PROJECT_PATH / 'outputs'
PROMETHEUS_PATH = PROJECT_PATH / 'prometheus'
PROMETHEUS_OPENMETRICS_PATH = PROMETHEUS_PATH / 'openMetrics'
PROMETHEUS_URL = "http://localhost:9090"
POSTGRESQL_DATA_PATH = "C:/Program Files/PostgreSQL/17/data"
POSTGRESQL_BIN_PATH = "C:/\"Program Files\"/PostgreSQL/17/bin"
DB_NAME = "weather"
DB_USER = "postgres"
DB_PASSWORD = "adb"
DB_HOST = "localhost"
DB_PORT = "5432"
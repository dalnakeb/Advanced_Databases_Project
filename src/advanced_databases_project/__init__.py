import os as _os
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent.absolute()
DATA_PATH = PROJECT_PATH / 'data'
OUTPUT_PATH = PROJECT_PATH / 'outputs'
PROMETHEUS_PATH = PROJECT_PATH / 'prometheus'
PROMETHEUS_OPENMETRICS_PATH = PROMETHEUS_PATH  / 'openMetrics'

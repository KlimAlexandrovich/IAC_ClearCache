import os

"""
Файл с конфигурационными переменными для работы приложения.
"""

LOGS_FILE_PATH = os.path.join(os.path.dirname(__file__), "logs", "logs.txt")
DEFAULT_LOGS_FILE = "logs.txt"
DRIVER_TIMEOUT = 10  # seconds
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

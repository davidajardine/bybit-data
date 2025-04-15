from datetime import datetime, timezone

# BYBIT Base API URL
BYBIT_BASE_URL = "https://api.bybit.com"

# Human-readable editable strings
START_DATE_STR = "2021-01-01T00:00:00"
END_DATE_STR = "2024-12-31T00:00:00"

# Auto-converted, centralized UTC datetime objects
START_DATE = datetime.fromisoformat(START_DATE_STR).replace(tzinfo=timezone.utc)
END_DATE = datetime.fromisoformat(END_DATE_STR).replace(tzinfo=timezone.utc)

# API settings
SYMBOL = "BTCUSDT"
INTERVAL = "1"  # 1-minute interval
INTERVAL_OI = "5min"  # 5-minute interval

# Table & DB
DB_PATH = "data/bybit_main.db"
TABLE_NAME = "bybit_main"

# Chunk sizes
CHUNK_SIZE = 200
CHUNK_SIZE_KLINE = 1000

TABLE_NAME_KLINE = "bybit_kline"
TABLE_NAME_OI = "bybit_oi"
TABLE_NAME_FUNDING = "bybit_funding"

# Bybit Data Ingestion Engine

This repository powers the data backend for ContextOS — a precision crypto trade analysis engine.  
It extracts 1-minute OHLCV, Open Interest, and Funding Rate data from Bybit's V5 API and merges them into a single time-aligned SQLite database for high-resolution backtesting and AI-driven trade setup classification.

---

##  Features

-  1-minute OHLCV (Kline) extraction
-  Open Interest (5m+) and Funding Rate capture
-  SQLite storage with chunked, reliable ingestion
-  Merge all streams into a unified `bybit_main` table
-  Modular logging with session-level visibility
-  Config-driven settings and resumption logic

---

## 🗂 Project Structure

```bash
bybit-data-ingestion/
│
├── config/                 # Centralized settings
│   └── settings.py
│
├── data/                   # Output SQLite DB
│   └── bybit_data.db
│
├── ingest/
│   ├── extract/            # API extractors
│   │   ├── funding_extractor.py
│   │   ├── kline_extractor.py
│   │   ├── oi_extractor.py
│   ├── load/               # SQLite writer
│   │   └── sqlite_loader.py
│   └── transform/          # Timestamp utilities
│       └── time_utils.py
│
├── logger.py               # Global logging utility
├── bybit_data.py           # Main ETL runner
├── merge_to_main.py        # Final unification script
```

## 🧠 How It Works

1. **Configure** your desired symbol, time range, and chunk sizes in `settings.py`.

2. **Run the ETL** pipeline:

   ```bash
   python bybit_data.py

This extracts and stores data into three SQLite tables:

bybit_kline
bybit_oi
bybit_funding

Merge the data into bybit_main:

  ```bash
  python merge_to_main.py
  ```

This resamples and forward-fills OI and funding rates into a clean 1-minute time series.

All settings live in `config/settings.py`, including:

```python
SYMBOL = "BTCUSDT"
INTERVAL = "1"
INTERVAL_OI = "5min"
START_DATE_STR = "2021-01-01T00:00:00"
END_DATE_STR = "2024-12-31T23:59:00"
CHUNK_SIZE = 200
TABLE_NAME = "bybit_kline"
DB_PATH = "data/bybit_data.db"
```

## 📄 License

MIT — open source, build your own terminal.  
Attribution welcome but not required.

## 👨‍💻 Built By

ContextOS – a self-hosted research tool for contextual crypto trade analysis  
Backtest smarter. Learn faster. Trust your setup.

import time
import requests
import pandas as pd
from logger import log
from config.settings import SYMBOL, INTERVAL, START_DATE, END_DATE, CHUNK_SIZE_KLINE, BYBIT_BASE_URL, TABLE_NAME_KLINE
from ingest.transform.time_utils import dt_to_ms, ms_to_dt
from ingest.load.sqlite_loader import load_to_sql

KLINE_ENDPOINT = "/v5/market/kline"

def extract_kline():
    start_ms = dt_to_ms(START_DATE)
    end_ms = dt_to_ms(END_DATE)

    all_rows = []

    while start_ms < end_ms:
        params = {
            "category": "linear",
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "start": start_ms,
            "end": min(start_ms + (CHUNK_SIZE_KLINE * 60_000), end_ms),
            "limit": CHUNK_SIZE_KLINE
        }

        resp = requests.get(BYBIT_BASE_URL + KLINE_ENDPOINT, params=params)
        data = resp.json()

        if data.get("retCode") != 0 or "result" not in data:
            log(f"Failed to fetch data: {data}", "ERROR")
            break

        candles = data["result"]["list"]
        if not candles:
            log("No more candles.", "INFO")
            break

        for row in candles:
            ts = int(row[0])
            all_rows.append({
                "timestamp": ts,
                "datetime": ms_to_dt(ts),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5]),
                "turnover": float(row[6])
            })

        log(f"Inserted {len(candles)} rows ending at {ms_to_dt(ts)}", "KLINE")
        start_ms += CHUNK_SIZE_KLINE * 60_000
        time.sleep(0.1)  # avoid rate limit

    df = pd.DataFrame(all_rows)
    df = df.sort_values("timestamp")

    load_to_sql(df, table_name=TABLE_NAME_KLINE, if_exists="replace")
    log(f"✅ Loaded {len(df)} total rows into {TABLE_NAME_KLINE}", "KLINE")

import time
import requests
import pandas as pd
from logger import log
from config.settings import SYMBOL, INTERVAL_OI, START_DATE, END_DATE, CHUNK_SIZE, BYBIT_BASE_URL, TABLE_NAME_OI
from ingest.transform.time_utils import dt_to_ms, ms_to_dt
from ingest.load.sqlite_loader import load_to_sql

OI_ENDPOINT = "/v5/market/open-interest"

def extract_open_interest():
    start_ms = dt_to_ms(START_DATE)
    end_ms = dt_to_ms(END_DATE)

    all_rows = []

    while start_ms < end_ms:
        params = {
            "category": "linear",
            "symbol": SYMBOL,
            "intervalTime": INTERVAL_OI,
            "startTime": start_ms,
            "endTime": min(start_ms + (CHUNK_SIZE * 60_000), end_ms),
            "limit": CHUNK_SIZE
        }

        resp = requests.get(BYBIT_BASE_URL + OI_ENDPOINT, params=params)
        data = resp.json()

        if data.get("retCode") != 0 or "result" not in data:
            log(f"OI fetch failed: {data}", "ERROR")
            break

        records = data["result"].get("list", [])
        if not records:
            log("[OI] No data returned in this chunk", "OI")
            start_ms += CHUNK_SIZE * 60_000
            continue

        for row in records:
            ts = int(row["timestamp"])
            all_rows.append({
                "timestamp": ts,
                "datetime": ms_to_dt(ts),
                "open_interest": float(row["openInterest"])
            })

        log(f"Inserted {len(records)} rows ending at {ms_to_dt(ts)}", "OI")
        start_ms += CHUNK_SIZE * 60_000
        time.sleep(0.1)

    df = pd.DataFrame(all_rows)
    df = df.sort_values("timestamp")

    load_to_sql(df, table_name=TABLE_NAME_OI, if_exists="replace")
    log(f"✅ Loaded {len(df)} total rows into {TABLE_NAME_OI}", "OI")

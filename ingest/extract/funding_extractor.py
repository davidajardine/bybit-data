import time
import requests
import pandas as pd
from logger import log
from config.settings import SYMBOL, INTERVAL, START_DATE, END_DATE, CHUNK_SIZE, BYBIT_BASE_URL, TABLE_NAME_FUNDING
from ingest.transform.time_utils import dt_to_ms, ms_to_dt
from ingest.load.sqlite_loader import load_to_sql

FUNDING_ENDPOINT = "/v5/market/funding/history"

def extract_funding_rates():
    start_ms = dt_to_ms(START_DATE)
    end_ms = dt_to_ms(END_DATE)

    all_rows = []

    while start_ms < end_ms:
        params = {
            "category": "linear",
            "symbol": SYMBOL,
            "startTime": start_ms,
            "endTime": min(start_ms + (CHUNK_SIZE * 60_000), end_ms),
            "limit": CHUNK_SIZE
        }

        resp = requests.get(BYBIT_BASE_URL + FUNDING_ENDPOINT, params=params)
        data = resp.json()

        if data.get("retCode") != 0 or "result" not in data:
            log(f"Funding fetch failed: {data}", "ERROR")
            break

        records = data["result"].get("list", [])
        if not records:
            log("No data returned in this chunk", "FUNDING")
            start_ms += CHUNK_SIZE * 60_000
            continue


        for row in records:
            ts = int(row["fundingRateTimestamp"])
            all_rows.append({
                "timestamp": ts,
                "datetime": ms_to_dt(ts),
                "funding_rate": float(row["fundingRate"])
            })

        log(f"Inserted {len(records)} rows ending at {ms_to_dt(ts)}", "FUNDING")
        start_ms += CHUNK_SIZE * 60_000
        time.sleep(0.1)

    df = pd.DataFrame(all_rows)
    df = df.sort_values("timestamp")

    load_to_sql(df, table_name=TABLE_NAME_FUNDING, if_exists="replace")
    log(f"✅ Loaded {len(df)} total rows into {TABLE_NAME_FUNDING}", "FUNDING")

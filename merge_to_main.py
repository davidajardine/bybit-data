import sqlite3
import pandas as pd
from datetime import datetime

from logger import log
from config.settings import DB_PATH

def merge_all_tables():
    log("🔁 Starting merge of kline, oi, and funding into bybit_main", "MERGE")

    conn = sqlite3.connect(DB_PATH)

    # Load source tables
    kline_df = pd.read_sql("SELECT * FROM bybit_kline", conn)
    oi_df = pd.read_sql("SELECT * FROM bybit_oi", conn)
    funding_df = pd.read_sql("SELECT * FROM bybit_funding", conn)

    # Convert and index by datetime
    for df in [kline_df, oi_df, funding_df]:
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("datetime", inplace=True)

    # Deduplicate before resampling
    oi_df = oi_df[~oi_df.index.duplicated(keep="last")]
    funding_df = funding_df[~funding_df.index.duplicated(keep="last")]

    # Resample OI and funding to 1-min resolution
    oi_resampled = oi_df[["open_interest"]].resample("1min").ffill()
    funding_resampled = funding_df[["funding_rate"]].resample("1min").ffill()


    # Start with kline (1m) as the base
    merged = kline_df.copy()
    merged = merged.join(oi_resampled, how="left")
    merged = merged.join(funding_resampled, how="left")

    # Final formatting
    merged.reset_index(inplace=True)
    merged["timestamp"] = merged["datetime"].astype("int64") // 1_000_000

    # Output
    merged.to_sql("bybit_main", conn, if_exists="replace", index=False)

    log(f"✅ Merged table bybit_main created with {len(merged)} rows", "MERGE")
    conn.close()

if __name__ == "__main__":
    merge_all_tables()

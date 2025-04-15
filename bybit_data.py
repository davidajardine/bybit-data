# main.py
import time
from datetime import datetime
import sys
from pathlib import Path
import os
from logger import log
from ingest.extract.kline_extractor import extract_kline
from ingest.extract.oi_extractor import extract_open_interest
from ingest.extract.funding_extractor import extract_funding_rates

# 🔧 Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

def run_all():
    log(f"🚀 Starting Bybit ETL Process", "SYSTEM")

    start = time.time()

    try:
        log(f"Starting Kline Extraction", "KLINE")
        extract_kline()
        log(f"✅ Kline Extraction Complete", "KLINE")

        log(f"Starting Open Interest Extraction", "OI")
        extract_open_interest()
        log(f"✅ Open Interest Extraction Complete", "OI")

        log(f"Starting Funding Rate Extraction", "FUNDING")
        extract_funding_rates()
        log(f"✅ Funding Rate Extraction Complete", "FUNDING")

    except Exception as e:
        log(f"❌ Error: {str(e)}", "ERROR")

    duration = round(time.time() - start, 2)
    log(f"✅ ETL Complete in {duration} seconds", "SYSTEM")

if __name__ == "__main__":
    run_all()

from datetime import datetime, timezone

# 🔁 Converts UTC datetime → ms timestamp
def dt_to_ms(dt):
    return int(dt.timestamp() * 1000)

# 🔁 Converts ms timestamp → UTC datetime
def ms_to_dt(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)

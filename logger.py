from datetime import datetime

def log(msg: str, tag: str = "INFO"):
    """
    [Logger] Prints timestamped logs with custom tag.
    """
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ts} - [{tag}] {msg}")

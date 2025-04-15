import sqlite3
import pandas as pd
from config.settings import DB_PATH

def load_to_sql(df, table_name: str, if_exists="append"):
    """
    Loads DataFrame into SQLite DB using to_sql.
    """
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)

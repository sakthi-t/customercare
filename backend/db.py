import os
import duckdb
from dotenv import load_dotenv
import pandas as pd

# load_dotenv()

def get_connection():
    # Your token is stored under ORDERS (per your earlier setup)
    token = os.getenv("ORDERS")
    if not token:
        raise ValueError("MotherDuck access token not found in .env (ORDERS).")

    # Optional override for DB name; defaults to 'my_db'
    db = os.getenv("MOTHERDUCK_DB", "my_db")

    # Connect to MotherDuck db with token
    return duckdb.connect(f"md:{db}?motherduck_token={token}")

def run_sql(query: str) -> pd.DataFrame:
    con = get_connection()
    return con.execute(query).fetchdf()

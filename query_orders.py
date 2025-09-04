import os
import duckdb
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
token = os.getenv("ORDERS")

if not token:
    raise ValueError("MotherDuck access token not found. Please set ORDERS in your .env file.")

# Connect to MotherDuck
# "md:" prefix tells DuckDB to connect to MotherDuck cloud
con = duckdb.connect(f"md:?motherduck_token={token}")

# Run a test query
query = "SELECT DISTINCT customer_name FROM my_db.main.orders;"
df = con.execute(query).df()

print("✅ Distinct Customers:")
print(df)

# Example Pandas queries
print("\n📊 First 5 Orders:")
df_orders = con.execute("SELECT * FROM my_db.main.orders LIMIT 5;").df()
print(df_orders)

print("\n📊 Orders by Status:")
df_status = con.execute("""
    SELECT status, COUNT(*) as total_orders
    FROM my_db.main.orders
    GROUP BY status
    ORDER BY total_orders DESC;
""").df()
print(df_status)

print("\n📊 Total Revenue per Customer:")
df_revenue = con.execute("""
    SELECT customer_name, SUM(price) as total_spent
    FROM my_db.main.orders
    GROUP BY customer_name
    ORDER BY total_spent DESC;
""").df()
print(df_revenue)

# 1️⃣ Fetch current status
df_before = con.execute("""
    SELECT order_id, customer_id, status
    FROM my_db.main.orders
    WHERE order_id = 1009 AND customer_id = 5;
""").df()
print("Before update:")
print(df_before)

# 2️⃣ Update status
con.execute("""
    UPDATE my_db.main.orders
    SET status = 'Delivered'
    WHERE order_id = 1009 AND customer_id = 5;
""")

# 3️⃣ Fetch after update
df_after = con.execute("""
    SELECT order_id, customer_id, status
    FROM my_db.main.orders
    WHERE order_id = 1009 AND customer_id = 5;
""").df()
print("\nAfter update:")
print(df_after)

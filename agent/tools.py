# agent/tools.py
import pandas as pd
import re
from backend.db import get_connection, run_sql
from backend import queries as q
from agent.responses import format_response

# Hardcoded roles
VALID_ADMIN = "John"

# --------------------------
# Predefined helper functions
# --------------------------

def get_total_orders():
    con = get_connection()
    return con.execute(q.TOTAL_ORDERS).fetchone()[0]

def get_cancelled_orders():
    con = get_connection()
    return con.execute(q.CANCELLED_ORDERS).fetchone()[0]

def get_order_status(order_id, customer_id):
    con = get_connection()
    return con.execute(q.ORDER_STATUS, [order_id, customer_id]).fetchone()

def update_order_status(order_id, customer_id, new_status):
    con = get_connection()
    con.execute(q.UPDATE_STATUS, [new_status, order_id, customer_id])
    return f"✅ Order {order_id} for customer {customer_id} updated to {new_status}."

# --------------------------
# Identity + validation
# --------------------------

def get_valid_customers():
    """Fetch the list of valid customers from DB dynamically."""
    df = run_sql("""
        SELECT customer_id, customer_name, customer_email
        FROM my_db.main.orders
        GROUP BY customer_id, customer_name, customer_email;
    """)
    return df.to_dict(orient="records")

def validate_identity(role: str, name: str, customer_id: str = None, email: str = None) -> bool:
    """Validate identity of customer or admin against DB or hardcoded admin."""
    if role == "admin":
        return name.strip().lower() == VALID_ADMIN.lower()
    elif role == "customer":
        customers = get_valid_customers()
        for c in customers:
            if (
                c["customer_name"].lower() == name.lower()
                and str(c["customer_id"]) == str(customer_id)
                and c["customer_email"].lower() == email.lower()
            ):
                return True
        return False
    return False

# --------------------------
# SQL Safety Guardrails
# --------------------------

def is_safe_sql(sql: str, role: str = "customer") -> bool:
    """
    Validate SQL to prevent destructive queries.
    - Customers: only SELECT.
    - Admin: SELECT or UPDATE (status only) with tight WHERE clause.
    """
    sql_clean = " ".join(sql.strip().upper().split())  # normalize spaces/case

    # Debug print
    print("\n--- SAFETY CHECK DEBUG ---")
    print(f"SQL being checked: {sql_clean}")
    print(f"Role: {role}")
    print("---------------------------\n")

    # Globally forbidden statements
    forbidden = [" DROP ", " TRUNCATE ", " ALTER ", " DELETE ", " INSERT "]
    if any(k in f" {sql_clean} " for k in forbidden):
        return False

    if role == "customer":
        # Customers can only run SELECT queries
        return sql_clean.startswith("SELECT")

    if role == "admin":
        if sql_clean.startswith("SELECT"):
            # ✅ allow all SELECT queries for admin
            return True
        if sql_clean.startswith("UPDATE"):
            # Guardrails: only update status on specific order with tight WHERE
            has_set_status = " SET STATUS " in sql_clean
            has_where = " WHERE " in sql_clean
            has_order_id = " ORDER_ID " in sql_clean
            has_customer_filter = (" CUSTOMER_ID " in sql_clean) or (" CUSTOMER_EMAIL " in sql_clean)
            return has_set_status and has_where and has_order_id and has_customer_filter
        return False

    return False

# --------------------------
# SQL Execution
# --------------------------

def execute_sql(sql: str, role: str = "customer") -> str:
    """
    Execute SQL query safely and return conversational response.
    - role: "customer" or "admin"
    - always returns a human-friendly string
    """

    # Normalize query: strip markdown fences + "sql " prefix if LLM added them
    sql = sql.strip()
    sql = re.sub(r"^```sql", "", sql, flags=re.IGNORECASE).strip()
    sql = re.sub(r"```$", "", sql).strip()
    if sql.lower().startswith("sql "):
        sql = sql[4:].strip()

    # 🔍 Debugging logs
    print("\n--- SQL DEBUG LOG ---")
    print(f"Cleaned SQL from LLM: {sql}")
    print(f"Role: {role}")
    print("---------------------\n")

    # ✅ Pass cleaned SQL to safety check
    if not is_safe_sql(sql, role):
        return f"⚠️ Unauthorized or unsafe query attempted: {sql}"

    try:
        df = run_sql(sql)
        print(f"✅ Executed successfully. Rows returned: {len(df)}")
        return format_response(df, role)
    except Exception as e:
        print(f"⚠️ Execution error: {e}")
        return f"⚠️ Query error: {e}"

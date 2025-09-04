# agent/workflow.py
from agent.llm import call_llm
from agent.tools import execute_sql, validate_identity
from agent.responses import empathetic_response

# Schema hint
SCHEMA = """
Table: my_db.main.orders
Columns: order_id, order_date, customer_id, customer_name, customer_email,
order_quantity, ordered_products, price, quantity, status
"""

# Track session identities
session_identity = {"role": None, "name": None, "customer_id": None, "email": None}

def identify_user(role: str, name: str, customer_id: str = None, email: str = None) -> str:
    """Validate and set session identity."""
    valid = validate_identity(role, name, customer_id, email)
    if not valid:
        if role == "admin":
            return f"🚫 Access denied. Only admin John is authorized, not {name}."
        elif role == "customer":
            return f"🚫 Sorry {name}, you are not a registered customer in our database."
    else:
        session_identity.update({"role": role, "name": name, "customer_id": customer_id, "email": email})
        if role == "admin":
            return f"👋 Welcome Admin {name}. You can view all records and update statuses."
        else:
            return f"👋 Hello {name}, I’ve verified your identity. I can help you with your orders."

def handle_query(query: str) -> str:
    """Main query handler with role + identity checks."""
    role = session_identity["role"]
    name = session_identity["name"]

    if role is None:
        return "⚠️ Please introduce yourself first (e.g., 'I am admin John' or 'I am Bob, my customer_id is 2, email is bob@example.com')."

    # Customers can only see their own data
    conditions = ""
    if role == "customer":
        cid = session_identity["customer_id"]
        email = session_identity["email"]
        conditions = f" WHERE customer_id={cid} AND customer_email='{email}'"

    # Build LLM prompt
    prompt = f"""
You are a SQL assistant for customer support.
Schema: {SCHEMA}
Role: {role}
User: {name}
Conditions for customer: {conditions}
Question: {query}

Generate a SAFE DuckDB SQL query.
- Customers: only SELECT on their own records (must include: {conditions}).
- Admin John: SELECT across all data or UPDATE status.
- Never use DROP, DELETE, TRUNCATE, ALTER, or INSERT.
- For UPDATE (admin only), only allow updating 'status' with a WHERE clause that includes order_id and either customer_id or customer_email.
Return only SQL.
"""
    sql = call_llm(prompt)

    # If customer, enforce their filter even if model forgot it
    if role == "customer" and sql.strip().upper().startswith("SELECT"):
        up = sql.upper()
        if " WHERE " not in up:
            sql = sql.rstrip(";") + conditions + ";"
        else:
            # If model added a WHERE, enforce customer_id + email
            if "CUSTOMER_ID" not in up or "CUSTOMER_EMAIL" not in up:
                sql = sql.rstrip(";") + f" AND customer_id={cid} AND customer_email='{email}';"

    # Execute safely (already returns conversational string)
    result = execute_sql(sql, role=role)

    # Conversational reply
    return empathetic_response(role, query, result)

import pandas as pd
def empathetic_delay_response(order_id):
    return (
        f"I understand your concern. Order {order_id} is currently in progress. "
        "We’re doing our best to ensure it reaches you soon. Thank you for your patience!"
    )

def polite_update_response(order_id, status):
    return f"Order {order_id} status has been updated to {status}. Thank you for checking in."

def empathetic_response(user_role: str, query: str, answer: str) -> str:
    if user_role == "customer":
        return f"😊 Dear customer, regarding your request: *{query}* → {answer}"
    else:  # admin
        return f"👨‍💼 Admin, here’s what I found for your query: *{query}* → {answer}"
    

def format_response(df: pd.DataFrame, role: str = "customer") -> str:
    """
    Convert a query result DataFrame into a conversational response.
    Role-specific formatting:
    - Customers: polite & personal
    - Admin: concise & professional
    """
    if df is None or df.empty:
        return "I couldn’t find any matching records."

    if "error" in df.columns:
        return f"⚠️ Query error: {df['error'][0]}"

    # If single scalar result
    if df.shape == (1, 1):
        value = df.iloc[0, 0]
        if role == "customer":
            return f"Here’s the information you requested: {value}."
        else:
            return f"Result: {value}"

    # If few rows (<=5)
    if len(df) <= 5:
        rows = df.to_dict(orient="records")
        if role == "customer":
            response = "Here are the details I found for you:\n"
        else:
            response = "Query returned the following records:\n"
        for r in rows:
            response += " • " + ", ".join([f"{k}: {v}" for k, v in r.items()]) + "\n"
        return response.strip()

    # If many rows
    if role == "customer":
        return f"I found {len(df)} records. Here are the first few:\n{df.head(5).to_string(index=False)}"
    else:
        return f"{len(df)} rows returned. Sample:\n{df.head(5).to_string(index=False)}"


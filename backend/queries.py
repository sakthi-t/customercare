TOTAL_ORDERS = "SELECT COUNT(*) FROM my_db.main.orders;"
CANCELLED_ORDERS = "SELECT COUNT(*) FROM my_db.main.orders WHERE status = 'Cancelled';"
ORDER_STATUS = "SELECT status FROM my_db.main.orders WHERE order_id = ? AND customer_id = ?;"
UPDATE_STATUS = "UPDATE my_db.main.orders SET status = ? WHERE order_id = ? AND customer_id = ?;"

# Some predefined queries the agent can fallback to
PREDEFINED = {
    "total_orders": "SELECT COUNT(*) as total_orders FROM my_db.main.orders;",
    "cancelled_orders": "SELECT COUNT(*) as cancelled_orders FROM my_db.main.orders WHERE status='Cancelled';",
    "delivered_orders": "SELECT COUNT(*) as delivered_orders FROM my_db.main.orders WHERE status='Delivered';"
}


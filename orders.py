import pandas as pd
import random
from faker import Faker

fake = Faker()

# Fixed customers
customers = [
    {"customer_id": 1, "customer_name": "John", "customer_email": "john@example.com"},
    {"customer_id": 2, "customer_name": "Alice", "customer_email": "alice@example.com"},
    {"customer_id": 3, "customer_name": "Bob", "customer_email": "bob@example.com"},
    {"customer_id": 4, "customer_name": "Mark", "customer_email": "mark@example.com"},
    {"customer_id": 5, "customer_name": "Maxwell", "customer_email": "maxwell@example.com"},
]

# Product catalog
products = ["Laptop", "Smartphone", "Headphones", "Tablet", "Camera", "Smartwatch", "Monitor"]

# Order statuses
statuses = ["In Progress", "Delivered", "Cancelled", "Returned", "Refunded"]

def generate_orders(num_orders, start_order_id=1000):
    data = []
    for i in range(num_orders):
        order_id = start_order_id + i
        order_date = fake.date_between_dates(date_start=pd.to_datetime("2025-01-01"),
                                             date_end=pd.to_datetime("2025-08-31"))
        customer = random.choice(customers)
        ordered_product = random.choice(products)
        quantity = random.randint(1, 5)
        price_per_unit = round(random.uniform(50, 2000), 2)  # product price
        price = round(price_per_unit * quantity, 2)
        status = random.choice(statuses)

        data.append({
            "order_id": order_id,
            "order_date": order_date,
            "customer_id": customer["customer_id"],
            "customer_name": customer["customer_name"],
            "customer_email": customer["customer_email"],
            "ordered_products": ordered_product,
            "order_quantity": 1,  # since we keep one product per row
            "quantity": quantity,
            "price": price,
            "status": status,
        })
    return pd.DataFrame(data)

# Generate datasets
df_small = generate_orders(100)
df_large = generate_orders(10000)

# Save to CSV
df_small.to_csv("orders_100.csv", index=False)
df_large.to_csv("orders_10000.csv", index=False)

print("Generated orders_100.csv and orders_10000.csv ✅")

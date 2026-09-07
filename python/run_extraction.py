from db import get_connection
from extract_purchase_orders import extract_purchase_orders
from extract_suppliers import extract_suppliers

connection = get_connection()

table = input("Enter the table name (purchase_orders or suppliers): ").strip().lower()

if table == "purchase_orders":
    data = extract_purchase_orders(connection)
elif table == "suppliers":
    data = extract_suppliers(connection)
else:
    data = None

connection.close()

if data is not None:
    print(f"Data from {table} table:")
    print(data)
else:
    print("Invalid table name. Please enter either 'purchase_orders' or 'suppliers'.")
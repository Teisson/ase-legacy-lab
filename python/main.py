from db import get_connection
from extract_purchase_orders import extract_purchase_orders
from extract_suppliers import extract_suppliers
from transform import transform_orders

connection = get_connection()

try:
    orders = extract_purchase_orders(connection)
    suppliers = extract_suppliers(connection)

    enriched_orders = transform_orders(suppliers, orders)

    print("Orders in:", len(orders))
    print("Orders out:", len(enriched_orders))
    print("First enriched order:")
    print(enriched_orders[0])

finally:
    connection.close()
  
assert len(orders) == len(enriched_orders)
assert "supplier_name" in enriched_orders[0]

print(len(orders))
print(len(enriched_orders))
print(enriched_orders[0])
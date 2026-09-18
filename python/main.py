from db import get_connection
from extract_purchase_orders import extract_purchase_orders
from extract_suppliers import extract_suppliers
from transform import transform_orders

connection = None

try:
    connection = get_connection()
    orders = extract_purchase_orders(connection)
    suppliers = extract_suppliers(connection)

    enriched_orders = transform_orders(suppliers, orders)

    assert len(orders) == len(enriched_orders)
    assert "supplier_name" in enriched_orders[0]

    print(f'Successfully enriched {len(enriched_orders)} orders with supplier names.')

except Exception as e:
    print(f'ETL pipeline failed: {e}')

finally:
    if connection is not None:
        connection.close()
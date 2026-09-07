from db import get_connection
from extract_purchase_orders import extract_purchase_orders
from extract_suppliers import extract_suppliers

connection = get_connection()

purchase_orders = extract_purchase_orders(connection)
suppliers = extract_suppliers(connection)

connection.close()
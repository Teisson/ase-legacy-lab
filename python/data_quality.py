def check_suppliers (suppliers):
    seen_supplier_ids = set()
    if not suppliers:
        raise ValueError("Suppliers list is empty.")
    for supplier in suppliers:
        if "supplier_id" not in supplier or "supplier_name" not in supplier:
            raise ValueError(f"Supplier data is missing required fields: {supplier}")
        supplier_id = supplier["supplier_id"]
        if supplier_id is None or supplier_id == "":
            raise ValueError(f"Supplier data has invalid supplier_id: {supplier}")
        elif supplier_id in seen_supplier_ids:
            raise ValueError(f"Duplicate supplier_id found: {supplier['supplier_id']}")
        seen_supplier_ids.add(supplier_id)

def check_orders(orders):
    seen_order_ids = set()
    if not orders:
        raise ValueError("Orders list is empty.")
    for order in orders:
        if "order_id" not in order or "supplier_id" not in order:
            raise ValueError(f"Order data is missing required fields: {order}") 
        order_id = order["order_id"]
        if order_id is None or order_id == "":
            raise ValueError(f"Order data has invalid order_id: {order}")
        elif order_id in seen_order_ids:
            raise ValueError(f"Duplicate order_id found: {order['order_id']}")
        seen_order_ids.add(order_id)
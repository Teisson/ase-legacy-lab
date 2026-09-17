def transform_orders(suppliers, orders):
    supplier_lookup = {}
    enriched_orders = []

    for supplier in suppliers:
        supplier_lookup[supplier["supplier_id"]] = supplier
 
    for order in orders:
        supplier = supplier_lookup[order["supplier_id"]]
        enriched_order = {**order, **supplier}
        enriched_orders.append(enriched_order)

    return enriched_orders

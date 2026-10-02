from db import get_connection
from extract_purchase_orders import extract_purchase_orders
from extract_suppliers import extract_suppliers
from data_quality import check_suppliers, check_orders, check_supplier_references
from transform import transform_orders
from google.cloud import bigquery
from load import load_enriched_orders

connection = None

try:
    connection = get_connection()
    orders = extract_purchase_orders(connection)
    suppliers = extract_suppliers(connection)

    check_suppliers(suppliers)
    check_orders(orders)
    check_supplier_references(suppliers, orders)

    enriched_orders = transform_orders(suppliers, orders)

    assert len(orders) == len(enriched_orders)
    assert "supplier_name" in enriched_orders[0]

    print(f'Successfully enriched {len(enriched_orders)} orders with supplier names.')

    bq_client = bigquery.Client(project="ase-legacy-lab")

    loaded_rows = load_enriched_orders(
        bq_client,
        enriched_orders
    )

    print(f"Successfully loaded {loaded_rows} rows to BigQuery.")

except Exception as e:
    print(f'ETL pipeline failed: {e}')
    raise e 

finally:
    if connection is not None:
        connection.close()
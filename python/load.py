from google.cloud import bigquery


TABLE_ID = "ase-legacy-lab.ase_legacy_data.enriched_purchase_orders"


def load_enriched_orders(client, enriched_orders):
    rows_to_load = []

    for order in enriched_orders:
        row = {
            "order_id": order["order_id"],
            "supplier_id": order["supplier_id"],
            "amount": str(order["amount"]),
            "order_date": order["order_date"].isoformat(),
            "supplier_name": order["supplier_name"],
            "country": order["country"],
        }

        rows_to_load.append(row)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        create_disposition=bigquery.CreateDisposition.CREATE_NEVER
    )

    load_job = client.load_table_from_json(
        rows_to_load,
        TABLE_ID,
        job_config=job_config,
    )

    load_job.result()

    return len(rows_to_load)

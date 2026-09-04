from db import get_connection

def extract_purchase_orders():
    """
    Extracts all rows from the "tester.purchase_orders" table and returns them as a list of dictionaries.

    Returns:
        list: A list of dictionaries where each dictionary represents a row in the "tester.purchase_orders" table.
    """

    # Establish a connection to the ASE database
    connection = get_connection()

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute a SQL query to retrieve all rows from the "tester.purchase_orders" table
    cursor.execute("SELECT * FROM tester.purchase_orders")
    rows = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [column[0] for column in cursor.description]

    # Create a list of dictionaries for all rows
    orders = [dict(zip(column_names, row)) for row in rows]  
    return orders  

# Call the function and print the result
orders = extract_orders()
print(orders)
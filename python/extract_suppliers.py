from db import get_connection

connection = get_connection()
print("Connection established successfully.")

cursor = connection.cursor()

cursor.execute("SELECT * FROM tester.suppliers")
rows = cursor.fetchall()
print(type(rows))
print(f"Number of rows fetched: {len(rows)}")
for row in rows:
    print(f"Supplier {row[0]}: {row[1]} ({row[2]})")  # Print the first three columns of each row in an ordered format

print(cursor.description)  # Print column names and types
print(cursor.description[0])  # Print the description of the first column
print(cursor.description[1][0])  # Print the name of the first column

column_names = [column[0] for column in cursor.description]
print(column_names)  # Print the list of column names

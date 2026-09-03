import os
import pyodbc
from dotenv import load_dotenv

#Loads environment variables from a .env file
load_dotenv()

ASE_USER = os.getenv("ASE_USER")
ASE_PASSWORD = os.getenv("ASE_PASSWORD")
ASE_DATABASE = os.getenv("ASE_DATABASE")
ASE_SERVER = os.getenv("ASE_SERVER")
ASE_HOST = os.getenv("ASE_HOST")
ASE_PORT = os.getenv("ASE_PORT")

print(f"Connecting to ASE database '{ASE_DATABASE}' on server '{ASE_SERVER}' at {ASE_HOST}:{ASE_PORT} with user '{ASE_USER}'")

# Connection string variable for connecting to the ASE database using FreeTDS driver
connection_string = (
    f"DRIVER={{FreeTDS}};"
    f"TDS_VERSION=5.0;"
    f"SERVER={ASE_HOST};"
    f"PORT={ASE_PORT};"
    f"DATABASE={ASE_DATABASE};"
    f"UID={ASE_USER};"
    f"PWD={ASE_PASSWORD};"
)

#pyodbc connection to the ASE database using the connection string
connection = pyodbc.connect(connection_string)

print("Connection established successfully.")

print(type(connection))
cursor = connection.cursor()
print(type(cursor))

cursor.execute("SELECT * FROM tester.suppliers")
rows = cursor.fetchone()

print("First row of the 'suppliers' table:")
print(rows)
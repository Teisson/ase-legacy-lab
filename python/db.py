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

#pyodbc function to connect to the ASE database using the connection string
def get_connection():
   connect = pyodbc.connect(connection_string)
   return connect
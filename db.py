import psycopg2 
import os
from dotenv import load_dotenv


load_dotenv()


connection_string = os.getenv('DATABASE_URL')

def get_db_connection():
    try:
        connection = psycopg2.connect(connection_string)
        print("Database connected successfully")
        return connection
    except Exception as error:
        print("Database connection error:", error)
        return None
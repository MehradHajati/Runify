#!/usr/bin/env python
import mysql.connector
from mysql.connector import Error
import config
import os

def run_schema():
    connection = None
    try:
        # Connect to the database using settings from config.py
        connection = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor(buffered=True)
            
            # Construct absolute path for schema.sql relative to this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            schema_file = os.path.join(script_dir, "schema.sql")
            with open(schema_file, "r") as file:
                sql_script = file.read()

            # Split the script into individual SQL statements (assuming ";" delimits statements)
            statements = sql_script.split(";")
            for statement in statements:
                statement = statement.strip()
                if statement:
                    print("Executing SQL:", statement)
                    cursor.execute(statement)
            
            connection.commit()
            print("Database setup complete!")
    except Error as e:
        print("Error while executing SQL script:", e)
    except FileNotFoundError as e:
        print("Error: schema.sql file not found. Ensure that schema.sql is in the same directory as init_db.py.", e)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    run_schema()
import os
import psycopg2
from app import settings


def create_and_populate_db():
    """Function to create and populate the database tables using the SQL script."""
    try:
        cnx = psycopg2.connect(user=settings.pg_user, password=settings.pg_password,
                                host=settings.pg_host, port=settings.pg_port, database=settings.pg_database)
        cur = cnx.cursor()
        
        # Read the SQL file
        with open('app\scripts\db_scripts\AskDB_Create_Tables.sql', 'r') as file:
            sql_commands = file.read()
            
        # Execute the SQL commands
        cur.execute(sql_commands)
        cnx.commit()
        print("Database created and populated successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
    finally:
        if cnx:
            cur.close()
            cnx.close()

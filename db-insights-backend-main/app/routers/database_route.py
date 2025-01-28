from fastapi import APIRouter, HTTPException
import psycopg2
from app import settings

database_router = APIRouter()

# Connect to the PostgreSQL database
db_connection: psycopg2.connect = psycopg2.connect(
    user=settings.pg_user,
    password=settings.pg_password,
    host=settings.pg_host,
    port=settings.pg_port,
    database=settings.pg_database,
)

db_cursor = db_connection.cursor()

@database_router.post("/create-database")
async def create_and_populate_db():
    """API endpoint to create and populate the database tables using the SQL script."""
    try:
        print(f'Database Connected: {db_connection}')

        # cur.execute("SELECT n.nspname FROM pg_namespace n WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema';")
        # rows = cur.fetchall()
        # print(f"Rows:  {rows}" )
        
        # Read the SQL file
        script_path = 'app/scripts/db_scripts/AskDB_Create_Tables.sql'
        with open(script_path, 'r') as file:
            sql_commands = file.read()
        
        # Execute the SQL commands
        db_cursor.execute(sql_commands)
        db_connection.commit()
        
        return {"message": "Database created and populated successfully!"}
    
    except Exception as e:
        # Rollback in case of error
        if db_connection:
            db_connection.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    finally:
        # Close connections
        if db_connection:
            db_cursor.close()
            db_connection.close()

@database_router.get("/api/db-insights/check-database")
async def check_db_connection():
    """API endpoint to CHECK the database Connectivity."""
    if db_connection:
        print(f'Database Connected: {db_connection}')

        return {"status": True}
    else:
        return {"status": False}

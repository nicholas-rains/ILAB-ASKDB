# src/yhatzi/tools/sql_tools.py
import logging
import time
from datetime import datetime
from typing import Any, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, create_engine
import json
from dotenv import load_dotenv
import os
from crewai.tools import BaseTool
from pydantic import PrivateAttr


from app import settings

# Load environment variables from .env
load_dotenv()

# Configuration Parameters
DATABASE_URL = f"postgresql://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.pg_database}"
POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 20))

def serialize_value(value: Any) -> Any:
    """
    Convert non-serializable values (e.g., datetime) to a JSON-serializable format.
    """
    if isinstance(value, datetime):
        return value.isoformat()
    return value

def serialize_row(row: Any, keys: Any) -> Dict[str, Any]:
    """
    Convert a SQLAlchemy Row object into a dictionary with serialized values.
    """
    return {key: serialize_value(value) for key, value in zip(keys, row)}

class ExecuteSQLTool(BaseTool):
    """
    Tool to execute SQL queries against a PostgreSQL database.
    """

    name: str = "execute_sql_query"
    description: str = "Executes a given SQL query against the PostgreSQL database and returns the results."

    _engine: Any = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)

        if not DATABASE_URL:
            logging.error("DATABASE_URL not found in environment variables.")
            raise ValueError("DATABASE_URL not set in environment variables.")

        # Create SQLAlchemy engine with connection pooling
        self._engine = create_engine(
            DATABASE_URL,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            pool_pre_ping=True
        )
        logging.info("SQLAlchemy engine initialized.")

    def _run(self, query: str) -> str:
        """
        Execute the SQL query and return the results as a JSON-formatted string.

        Parameters:
            query (str): The SQL query to execute.

        Returns:
            str: JSON-formatted string containing the results or an error message.
        """
        logging.info(f"Executing SQL Query: {query}")
        start_time = time.time()

        # Attempt to parse the query if it's a JSON string
        try:
            input_data = json.loads(query)
            sql_query = input_data.get('query')
            if not sql_query:
                logging.error("No 'query' key found in the input data.")
                return json.dumps({
                    "error": "No 'query' key found in the input data."
                }, indent=4)
        except json.JSONDecodeError:
            # If it's not a JSON string, treat it as a raw SQL query
            sql_query = query

        # Clean the query string
        sql_query = sql_query.replace("\\n", " ").strip('"').strip("'").strip()
        logging.debug(f"Cleaned SQL Query: {sql_query}")

        try:
            with self._engine.connect() as conn:
                conn.execute(text("SET search_path TO ask_data, public"))
                result = conn.execute(text(sql_query))
                rows = result.fetchall()
                keys = result.keys()
            elapsed_time = time.time() - start_time
            serialized_results = [serialize_row(row, keys) for row in rows]
            logging.info(f"Query executed successfully in {elapsed_time:.2f} seconds. Rows fetched: {len(serialized_results)}")
            
            if serialized_results:
                # Wrap results under "Query_1" key
                response = {
                    "Query_1": serialized_results
                }
                # Structure the final output as per the desired JSON format
                final_output = {
                    "query": sql_query,
                    "response": response
                }
                return json.dumps(final_output, indent=4)
            else:
                # Return a clear message if no data is found
                final_output = {
                    "query": sql_query,
                    "response": {
                        "message": "No data found."
                    }
                }
                return json.dumps(final_output, indent=4)
        except SQLAlchemyError as e:
            logging.error(f"Error executing query: {e}")
            final_output = {
                "query": sql_query,
                "response": {
                    "error": str(e)
                }
            }
            return json.dumps(final_output, indent=4)

    def _arun(self, query: str) -> str:
        """
        Asynchronous run method. Not implemented.
        """
        raise NotImplementedError("ExecuteSQLTool does not support async operations.")

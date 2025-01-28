# src/oneaskdb/main.py
import sys

from fastapi import HTTPException

from app.crews.crew_nlp_to_sql.nlp_to_sql_crew import NlpToSqlCrew
from app.schemas.schema import get_schema
import json
import logging
import sqlparse
from typing import List

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize the Crew once and make it accessible
crew_instance =  NlpToSqlCrew().crew()

def extract_table_names(sql_query: str) -> List[str]:
    """
    Extract table names from a SQL query using sqlparse.
    
    Args:
        sql_query (str): The SQL query to parse
        
    Returns:
        List[str]: List of unique table names used in the query
    """
    if not sql_query:
        return []
        
    # Parse the SQL query
    parsed = sqlparse.parse(sql_query)[0]
    
    # Initialize a set to store unique table names
    tables = set()
    
    # Function to recursively extract table names from tokens
    def extract_from_tokens(tokens):
        for token in tokens:
            if isinstance(token, sqlparse.sql.Token) and token.value.upper() == 'FROM':
                # Get the next token after FROM
                idx = tokens.index(token) + 1
                while idx < len(tokens):
                    next_token = tokens[idx]
                    if isinstance(next_token, sqlparse.sql.Identifier):
                        tables.add(next_token.get_real_name())
                    elif isinstance(next_token, sqlparse.sql.Token) and next_token.value.upper() == 'JOIN':
                        # Get the table name after JOIN
                        if idx + 1 < len(tokens):
                            join_token = tokens[idx + 1]
                            if isinstance(join_token, sqlparse.sql.Identifier):
                                tables.add(join_token.get_real_name())
                    idx += 1
            elif hasattr(token, 'tokens'):
                extract_from_tokens(token.tokens)
    
    extract_from_tokens(parsed.tokens)
    return sorted(list(tables))

def crewai_chat(user_query: str) -> dict:
    """
    Processes the user query through CrewAI and returns the AI-generated SQL query, results, and QA report.

    Args:
        user_query (str): The natural language query from the user.

    Returns:
        dict: A dictionary containing the SQL query, its results, the rewritten query, and the QA report.
    """
    try:
        refined_query = user_query  # Initial refined query is the user query

        # Prepare the inputs for the crew
        inputs = {
            'user_query': refined_query,
            'schema': get_schema(),
        }

        logger.info("Kicking off the CrewAI process.")

        try:
            # Kickoff the crew to execute all tasks sequentially
            crew_instance.kickoff(inputs=inputs)
        except Exception as e:
            logger.error(f"Error during CrewAI kickoff: {e}", exc_info=True)
            return {
                "original_query": user_query,
                "query": "",
                "response": {},
                "qa_status": "Error",
                "qa_message": "Failed to process the query.",
                "rewritten_query": ""
            }

        # Read the output files
        try:
            with open("app/data/responses/rewritten_query.txt", "r") as f:
                refined_query = f.read().strip()
                logger.info("Refined query read successfully.")
        except FileNotFoundError:
            refined_query = ""
            logger.warning("Refined query file not found.")

        try:
            with open("app/data/responses/generated_sql.json", "r") as f:
                sql_response = json.load(f)
                ai_query = sql_response.get("query", "")
                ai_data = sql_response.get("response", {})
                # Extract table names from the SQL query
                used_tables = extract_table_names(ai_query)
                logger.info(f"Tables used in query: {used_tables}")
        except FileNotFoundError:
            ai_query = ""
            ai_data = {}
            used_tables = []
            logger.warning("Generated SQL query file not found.")

        try:
            with open("app/data/responses/sql_qa_report.json", "r") as f:
                qa_report = json.load(f)
                logger.info("QA report read successfully.")
        except FileNotFoundError:
            qa_report = {
                "status": "Error",
                "message": "QA report not found."
            }
            logger.warning("QA report file not found.")
        except json.JSONDecodeError:
            qa_report = {
                "status": "Error",
                "message": "QA report contains invalid JSON."
            }
            logger.error("QA report file contains invalid JSON.")

        # Return the response as a dictionary
        return {
            "original_query": user_query,
            "query": ai_query.replace("\\n", " "),
            "response": ai_data,
            "qa_status": qa_report.get("status"),
            "qa_message": qa_report.get("message"),
            "rewritten_query": refined_query,
            "used_tables": used_tables
        }

    except Exception as err:
        # Catch any errors and return a structured error response
        error_details = {
            "error": "An unexpected error occurred",
            "details": str(err),
            "type": type(err).__name__,
            "module": __name__,
            "line": sys.exc_info()[-1].tb_lineno
        }
        raise HTTPException(status_code=422, detail=error_details)

# src/yhatzi/tools/retrieval_tool.py

import logging
import json
from typing import Any, List, Type
from sqlalchemy import text, create_engine
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
import os
from openai import AzureOpenAI, OpenAIError
from datetime import datetime

class EmbeddingRetrievalToolInput(BaseModel):
    user_query: str = Field(..., description="The user's refined query for semantic search.")

class EmbeddingRetrievalTool(BaseTool):
    """
    Tool to retrieve data using vector similarity search on embedding columns across all relevant tables.
    """

    name: str = "embedding_retrieval_tool"
    description: str = "Retrieves data using vector similarity search on embedding columns."
    args_schema: Type[BaseModel] = EmbeddingRetrievalToolInput

    _engine: Any = PrivateAttr()
    _embedding_deployment: str = PrivateAttr()
    _client: Any = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._engine = create_engine(os.getenv("DATABASE_URL"))

        # Azure OpenAI API configuration with `api_key`, `api_version`, and `azure_endpoint`
        self._client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

        self._embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

        # List of tables to search
        self._tables_with_embeddings = [
            "account",
            "account_x_customer_rltnp",
            "customer",
            "customer_details",
            "customer_idntfctn",
            "deposit",
        ]

    def _run(self, user_query: str) -> str:
        """
        Perform vector similarity search using the user's query across relevant tables.
        """
        logging.info("Starting retrieval using EmbeddingRetrievalTool.")

        # Compute the embedding of the user query
        try:
            response = self._client.embeddings.create(
                input=user_query,
                model=self._embedding_deployment  # Correct keyword for Azure model
            )
            query_embedding = response.data[0].embedding
        except OpenAIError as e:
            logging.error(f"Error computing embedding: {e}")
            return json.dumps({"error": f"Error computing embedding: {e}"})
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return json.dumps({"error": f"Unexpected error: {e}"})

        # Convert embedding to PostgreSQL array format
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'

        retrieved_data = {}

        # Open a file to log the output
        with open('retrieval_output.log', 'w') as output_file:
            for table in self._tables_with_embeddings:
                # Define the SQL query for vector similarity search
                sql_query = text(f"""
                SELECT *, 1 - (embedding <#> :embedding) AS similarity
                FROM {table}
                ORDER BY embedding <#> :embedding LIMIT 10;
                """)

                try:
                    # Execute the query
                    with self._engine.connect() as conn:
                        result = conn.execute(sql_query, {'embedding': embedding_str})
                        rows = [dict(row._mapping) for row in result]

                        # Handle datetime serialization for JSON output
                        for row in rows:
                            for key, value in row.items():
                                if isinstance(value, datetime):
                                    row[key] = value.isoformat()

                        logging.info(f"Retrieval query executed successfully for table '{table}'.")
                        if rows:
                            retrieved_data[table] = rows
                        # Write the result to the output file
                        output_file.write(f"Results for table '{table}':\n")
                        output_file.write(json.dumps(rows, indent=4) + "\n\n")
                except Exception as e:
                    logging.error(f"Error executing retrieval query on table '{table}': {e}")
                    output_file.write(f"Error executing retrieval query on table '{table}': {e}\n\n")

        # Return the retrieved data
        output = {
            "retrieved_data": retrieved_data
        }
        return json.dumps(output, indent=4)

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Asynchronous execution not implemented.")

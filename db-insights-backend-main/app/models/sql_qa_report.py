# app/models/sql_response.py

from pydantic import BaseModel

class SQLQAResponse(BaseModel):
    status: str
    message: str

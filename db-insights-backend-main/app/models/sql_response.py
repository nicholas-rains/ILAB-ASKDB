# app/models/sql_response.py

from pydantic import BaseModel
from typing import Dict, List, Any

class SQLResponse(BaseModel):
    query: str
    response: Dict[str, List[Dict[str, Any]]]

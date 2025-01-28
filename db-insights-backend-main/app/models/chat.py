# app/models/chat.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ChatInput(BaseModel):
    query: str
    session_id: Optional[UUID] = None
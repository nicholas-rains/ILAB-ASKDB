# app/routers/chat.py
import sys

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.models.chat import ChatInput  # Import the Pydantic model for the request
from app.services.crew_service import crewai_chat  # Fixed import path


chat_router = APIRouter()

@chat_router.post("/api/db-insights/chat", response_class=JSONResponse)
async def handle_chat_query(request: Request, data: ChatInput):
    try:
        # Extract the user query from the incoming request
        user_query = data.query
        print(f"Received user query: {user_query}")

        # Call the CrewAI logic to process the query
        result = crewai_chat(user_query)

        # Extract all necessary data from the result
        ai_query = result.get("query", "")
        ai_data = result.get("response", {})
        qa_status = result.get("qa_status", "")
        qa_message = result.get("qa_message", "")
        rewritten_query = result.get("rewritten_query", "")
        used_tables = result.get("used_tables", [])

        # Return the complete response to the frontend
        return JSONResponse(content={
            "query": ai_query.replace("\\n", " "),
            "response": ai_data,
            "qa_status": qa_status,
            "qa_message": qa_message,
            "rewritten_query": rewritten_query,
            "used_tables": used_tables
        })

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

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
import json
import logging

from app.utils import email_utils
from app.config.email_config import RECIPIENTS

logger = logging.getLogger(__name__)

email_router = APIRouter()

@email_router.post("/api/db-insights/share", response_class=JSONResponse)
async def handle_share_request(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint to handle sharing the query results via email.
    """
    try:
        data = await request.json()
        original_query = data.get("original_query", "")
        rewritten_query = data.get("rewritten_query", "").split("\n")[0]  # Only take the first line
        sql_query = data.get("sql_query", "")
        sql_results = data.get("sql_results", {})
        used_tables = data.get("used_tables", [])

        logger.info(f"Received share request for query: {original_query}")

        # Prepare the email content with a cleaner format
        email_subject = "Database Query Results"
        email_body = f"""
        <html>
          <body>
            <h3>Original Query</h3>
            <p>{original_query}</p>
            
            <h3>Improved Query Interpretation</h3>
            <p>{rewritten_query}</p>
            
            <h3>SQL Query</h3>
            <pre>{sql_query}</pre>
            
            <h3>Tables Used</h3>
            <p>{', '.join(used_tables)}</p>
            
            <h3>Results</h3>
            <pre>{json.dumps(sql_results, indent=2)}</pre>
          </body>
        </html>
        """

        if not RECIPIENTS:
            logger.error("No email recipients defined.")
            return JSONResponse(content={"status": "No email recipients defined."}, status_code=500)

        # Add email sending to background tasks
        background_tasks.add_task(
            email_utils.send_email,
            subject=email_subject,
            body=email_body,
            recipients=RECIPIENTS
        )

        return JSONResponse(content={"status": "Email sent successfully."})
    
    except Exception as err:
        logger.error(f"Error handling chat query: {err}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(err))

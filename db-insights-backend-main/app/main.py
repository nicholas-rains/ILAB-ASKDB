# app/main.py
from logging.handlers import RotatingFileHandler

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.chat import chat_router
from app.routers.database_route import database_router
import logging
import os

db_insights_service = FastAPI()

# Include the API router
db_insights_service.include_router(chat_router, prefix="/api/askdb")
db_insights_service.include_router(database_router)

# Configure logging with RotatingFileHandler
LOG_FILE = os.getenv("LOG_FILE", "app/logs/execution.log")
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logger = logging.getLogger(__name__)


# CORS configuration to allow requests from the frontend
origins = ["*"]

db_insights_service.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(db_insights_service, host="0.0.0.0", port=5070)


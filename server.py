""" Server module """
import logging
import os

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.responses import HTMLResponse, Response

from app.api.api import api_router
from app.core.config import settings
from app.core.utils import JSONFormatter, CustomFormatter


app = FastAPI(
    docs_url="/docs",
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)


@app.on_event("startup")
async def startup_event():
    """Configure logging on startup"""
    # Configure uvicorn access logger
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    
    # Configure uvicorn main logger
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()
    
    # Create handler with appropriate formatter
    handler = logging.StreamHandler()
    
    log_format = os.getenv("LOG_FORMAT", "text").lower()
    if log_format == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(CustomFormatter())
    
    # Set log level
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level, logging.INFO)
    
    access_logger.addHandler(handler)
    access_logger.setLevel(level)
    
    uvicorn_logger.addHandler(handler)
    uvicorn_logger.setLevel(level)
    
    # Configure FastAPI logger
    app_logger = logging.getLogger("plumbus_image_gen")
    app_logger.handlers.clear()
    app_logger.addHandler(handler)
    app_logger.setLevel(level)
    
    app_logger.info("Plumbus Image Generation Service started", extra={
        "service": "plumbus_image_gen",
        "version": settings.VERSION,
        "log_format": log_format,
        "log_level": log_level
    })


app.include_router(api_router)


@app.get("/health")
async def health():
    return "OK"

@app.get("/", response_class=HTMLResponse)
async def index():
    return open("app/tpl/index.html").read()

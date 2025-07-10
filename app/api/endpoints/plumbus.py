from typing import Any
import time
import uuid

from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.responses import FileResponse

from app import models
from app.core.config import settings

from app.plumbus import PlumbusDrawer
from app.models import PlumbusModel
from app.core.utils import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("")
async def generate_plumbus(
    plumbus: PlumbusModel
) -> Any:
    """Generate a plumbus image based on the provided model"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    logger.info("Received plumbus generation request", extra={
        "request_id": request_id,
        "plumbus_model": plumbus.dict(),
        "endpoint": "/plumbus",
        "start_time": start_time
    })
    
    try:
        drawer = PlumbusDrawer(plumbus)
        filename = drawer.draw()
        
        generation_time = time.time() - start_time
        
        logger.info("Plumbus generation request completed successfully", extra={
            "request_id": request_id,
            "generated_filename": filename,
            "generation_time_seconds": round(generation_time, 3),
            "plumbus_model": plumbus.dict()
        })
        
        return FileResponse(filename, media_type="image/png")
        
    except HTTPException as e:
        logger.error("HTTP exception during plumbus generation", extra={
            "request_id": request_id,
            "error_code": e.status_code,
            "error_detail": e.detail,
            "plumbus_model": plumbus.dict(),
            "generation_time_seconds": round(time.time() - start_time, 3)
        })
        raise
        
    except Exception as e:
        logger.error("Unexpected error during plumbus generation", extra={
            "request_id": request_id,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "plumbus_model": plumbus.dict(),
            "generation_time_seconds": round(time.time() - start_time, 3)
        })
        raise HTTPException(status_code=500, detail="Internal server error during plumbus generation")

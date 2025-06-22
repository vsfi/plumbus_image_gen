from typing import Any

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
async def genetate_plumbus(
    plumbus: PlumbusModel
) -> Any:
    logger.info(plumbus)
    drawer = PlumbusDrawer(plumbus)
    filename = drawer.draw()
    return FileResponse(filename, media_type="image/png")

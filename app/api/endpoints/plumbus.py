from typing import Any

from fastapi import APIRouter, Body, HTTPException, Depends

from app import models
from app.core.config import settings

from app.plumbus import PlumbusDrawer
from app.models import PlumbusModel
from app.core.utils import logger


router = APIRouter()

@router.post("")
async def genetate_plumbus(
    plumbus: PlumbusModel
) -> Any:
    logger.info(plumbus)
    drawer = PlumbusDrawer(plumbus)
    result = drawer.draw()
    return {"success": result}
""" Server module """
import logging

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.responses import HTMLResponse, Response

from app.api.api import api_router
from app.core.config import settings


app = FastAPI(
    docs_url="/docs",
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def index():
    return open("app/tpl/index.html").read()

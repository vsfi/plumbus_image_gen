from fastapi import APIRouter, Depends

from app.api.endpoints import plumbus

api_router = APIRouter()
api_router.include_router(
    plumbus.router,
    prefix="/plumbus",
    tags=["Plumbus"],
)
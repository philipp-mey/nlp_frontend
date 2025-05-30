from fastapi import APIRouter

from .upload import router as upload_router

v1_router = APIRouter()
v1_router.include_router(upload_router)

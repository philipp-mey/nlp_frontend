from fastapi import APIRouter

from .upload import router as upload_router
from .video import router as video_router

v1_router = APIRouter()
v1_router.include_router(upload_router)
v1_router.include_router(video_router)

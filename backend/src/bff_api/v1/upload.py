import os
import shutil

from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import JSONResponse
from src.processing.pipeline import process_video

UPLOAD_DIRECTORY = "media/uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

router = APIRouter()


@router.post("/upload/")
async def upload_video(
    video: UploadFile = File(...),
    target_lang: str = Form(...),
    background_tasks: BackgroundTasks = None,
) -> JSONResponse:
    """
    Upload a video file and process it in the background.

    Args:
        video (UploadFile): The video file being uploaded.
        target_lang (str): Target language for subtitle translation (from form field).
        background_tasks (BackgroundTasks): FastAPI background tasks.

    Returns:
        JSONResponse: Upload confirmation.
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, video.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        if background_tasks:
            background_tasks.add_task(process_video, file_path, target_lang)
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Video uploaded! Processing in background (target language: {target_lang}).",
                "filename": video.filename,
                "saved_path": file_path,
                "target_lang": target_lang,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Could not save video: {e}"
        )
    finally:
        await video.close()

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from src.logic.audio import extract_audio
from src.logic.transcription import generate_subtitle_file, transcribe
from src.logic.translation import translate_srt

MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)

router = APIRouter()


@router.post("/upload/")
async def upload_video(
    file: UploadFile = File(...), target_language: str = Form(...)
):
    video_id = str(uuid.uuid4())
    video_ext = Path(file.filename).suffix
    video_name = f"{video_id}{video_ext}"
    video_path = MEDIA_DIR / video_name

    with open(video_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        audio_path = extract_audio(str(video_path))
        language, segments = transcribe(audio_path)
        original_srt_path = MEDIA_DIR / f"{video_id}.{language}.srt"
        generate_subtitle_file(str(video_path), language, segments)
        shutil.move(f"{video_path.stem}.{language}.srt", original_srt_path)
        translated_srt_path = MEDIA_DIR / f"{video_id}.{target_language}.srt"
        translate_srt()

        with open(original_srt_path, "r", encoding="utf-8") as f:
            original_text = f.read()
        with open(translated_srt_path, "r", encoding="utf-8") as f:
            translated_text = f.read()

        return {
            "video_id": video_id,
            "video_url": f"/media/{video_name}",
            "language": language,
            "original_srt_url": f"/media/{original_srt_path.name}",
            "translated_srt_url": f"/media/{translated_srt_path.name}",
            "original_text": original_text,
            "translated_text": translated_text,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

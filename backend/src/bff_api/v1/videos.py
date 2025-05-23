from pathlib import Path

from fastapi import APIRouter

MEDIA_DIR = Path("media")
router = APIRouter()


@router.get("/videos/")
def list_videos():
    videos = []
    for video_file in MEDIA_DIR.glob("*.mp4"):
        video_id = video_file.stem
        original_srt = next(MEDIA_DIR.glob(f"{video_id}.*.srt"), None)
        translated_srt = None
        for srt in MEDIA_DIR.glob(f"{video_id}.*.srt"):
            if srt != original_srt:
                translated_srt = srt
                break
        original_text = (
            original_srt.read_text(encoding="utf-8") if original_srt else ""
        )
        translated_text = (
            translated_srt.read_text(encoding="utf-8")
            if translated_srt
            else ""
        )
        videos.append(
            {
                "name": video_file.name,
                "video_url": f"/media/{video_file.name}",
                "language": original_srt.name.split(".")[1]
                if original_srt
                else "",
                "original_srt_url": f"/media/{original_srt.name}"
                if original_srt
                else "",
                "translated_srt_url": f"/media/{translated_srt.name}"
                if translated_srt
                else "",
                "original_text": original_text,
                "translated_text": translated_text,
            }
        )
    return {"videos": videos}

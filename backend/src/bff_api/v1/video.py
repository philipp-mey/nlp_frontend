from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException,
)

router = APIRouter()


@router.get("/videos/")
async def list_videos():
    """
    List all processed videos with their metadata.

    Returns:
        JSONResponse: List of processed videos with their information.
    """
    try:
        processed_dir = Path("media/processed")
        videos = []

        if processed_dir.exists():
            # Look for UUID folders in processed directory
            for uuid_folder in processed_dir.iterdir():
                if uuid_folder.is_dir():
                    # Find video files in each UUID folder
                    video_files = []
                    for ext in [
                        "*.mp4",
                        "*.avi",
                        "*.mov",
                        "*.mkv",
                        "*.webm",
                        "*.flv",
                    ]:
                        video_files.extend(uuid_folder.glob(ext))

                    for video_file in video_files:
                        # Find associated subtitle files
                        base_name = video_file.stem
                        srt_files = list(uuid_folder.glob(f"{base_name}*.srt"))

                        videos.append(
                            {
                                "video_id": uuid_folder.name,
                                "name": video_file.name,
                                "path": str(
                                    video_file.relative_to(Path("media"))
                                ),
                                "full_path": str(video_file),
                                "subtitle_count": len(srt_files),
                                "created_at": video_file.stat().st_mtime,
                            }
                        )

        # Sort by creation time (newest first)
        videos.sort(key=lambda x: x["created_at"], reverse=True)

        return {"videos": videos, "total": len(videos)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to list videos: {str(e)}"
        )


@router.get("/videos/{video_id}/subtitles")
async def get_video_subtitles(video_id: str):
    """
    Get available subtitle files for a specific video.

    Args:
        video_id (str): UUID of the processed video folder.

    Returns:
        JSONResponse: List of available subtitle files.
    """
    try:
        video_folder = Path("media/processed") / video_id

        if not video_folder.exists():
            raise HTTPException(status_code=404, detail="Video not found")

        # Find all SRT files
        srt_files = list(video_folder.glob("*.srt"))
        subtitles = []

        for srt_file in srt_files:
            filename = srt_file.name

            # Determine language from filename
            if filename.count(".") >= 2:  # e.g., "video.de.srt"
                lang_code = filename.split(".")[-2]
                if len(lang_code) == 2:  # Valid language code
                    language = get_language_name(lang_code)
                    subtitle_type = "translated"
                else:
                    language = "Original"
                    subtitle_type = "original"
            else:  # e.g., "video.srt"
                language = "Original"
                subtitle_type = "original"

            subtitles.append(
                {
                    "filename": filename,
                    "language": language,
                    "language_code": lang_code
                    if "lang_code" in locals()
                    else "original",
                    "type": subtitle_type,
                    "path": str(srt_file.relative_to(Path("media"))),
                    "size": srt_file.stat().st_size,
                }
            )

        return {"subtitles": subtitles, "video_id": video_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get subtitles: {str(e)}"
        )


def get_language_name(code: str) -> str:
    """Convert language code to language name."""
    language_map = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "nl": "Dutch",
        "ar": "Arabic",
        "hi": "Hindi",
    }
    return language_map.get(code.lower(), code.upper())

import logging
from pathlib import Path
from typing import Optional

import ffmpeg

logger = logging.getLogger(__name__)


def extract_audio_from_video(
    video_path_str: str,
) -> Optional[str]:
    """
    Extracts audio from a video file and saves it as a WAV file.

    The audio is extracted in WAV format, 16kHz sample rate, mono channel.
    The output audio file is saved in the same directory as the input video
    file, with the same base name but a '.wav' extension.

    Args:
        video_path_str: The absolute or relative path to the input video file.

    Returns:
        The path (as a string) to the extracted audio file if successful,
        otherwise None.
    """
    video_file = Path(video_path_str)
    audio_file = video_file.with_suffix(".wav")

    if not video_file.is_file():
        logger.error("Input video file not found: %s", video_file)
        return None

    try:
        logger.info(
            "Attempting to extract audio from '%s' to '%s'",
            video_file,
            audio_file,
        )

        audio_file.parent.mkdir(parents=True, exist_ok=True)

        process = (
            ffmpeg.input(str(video_file))
            .output(
                str(audio_file),
                acodec="pcm_s16le",
                ar="16000",
                ac=1,
            )
            .overwrite_output()
        )

        process.run(capture_stdout=True, capture_stderr=True, quiet=True)

        logger.info("Audio extracted successfully: %s", audio_file)
        return str(audio_file)

    except ffmpeg.Error as e:
        ffmpeg_stderr = (
            e.stderr.decode("utf-8", errors="ignore").strip()
            if e.stderr
            else "No stderr."
        )
        logger.error(
            "FFmpeg error during audio extraction for '%s'. FFmpeg stderr: %s",
            video_file,
            ffmpeg_stderr,
        )
        return None
    except Exception as e:
        logger.error(
            "An unexpected Python error occurred during audio extraction for '%s': %s",
            video_file,
            e,
            exc_info=True,
        )
        return None

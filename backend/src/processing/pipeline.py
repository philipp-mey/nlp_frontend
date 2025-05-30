import logging
import os

from src.services.audio import extract_audio_from_video
from src.services.srt_writer import (
    generate_srt_file,
    generate_translated_srt_file,
)
from src.services.transcription import transcribe

logger = logging.getLogger(__name__)


def process_video(file_path: str, target_lang: str) -> None:
    """
    Complete processing pipeline:
    1. Extract audio from video
    2. Transcribe audio to subtitles
    3. Translate subtitles to the target language
    4. Write translated subtitles to an SRT file

    Args:
        file_path (str): Path to the input video file.
        target_lang (str): Target language code for subtitle translation.

    Raises:
        RuntimeError: If any step fails.
    """
    logger.info("Starting processing for video: %s", file_path)
    base, _ = os.path.splitext(file_path)
    srt_path = f"{base}.srt"
    translated_srt_path = f"{base}.{target_lang}.srt"
    # 1. Extract audio
    try:
        audio_path: str = extract_audio_from_video(file_path)
        logger.info("Audio extracted to %s", audio_path)
    except Exception as e:
        logger.error("Audio extraction failed: %s", e, exc_info=True)
        raise RuntimeError("Audio extraction failed") from e

    # 2. Transcribe audio
    try:
        source_lang, segments = transcribe(audio_path, model_size="small")
        logger.info("Transcription complete: %d segments", len(segments))
    except Exception as e:
        logger.error("Transcription failed: %s", e, exc_info=True)
        raise RuntimeError("Transcription failed") from e

    # 3. Generate original SRT file
    try:
        generate_srt_file(segments, srt_path, source_lang)
        logger.info("SRT file written: %s", srt_path)
    except Exception as e:
        logger.error("SRT writing failed: %s", e, exc_info=True)
        raise RuntimeError("SRT writing failed") from e

    # 4. Generate translated SRT file
    try:
        generate_translated_srt_file(
            segments, translated_srt_path, source_lang, target_lang
        )
        logger.info("SRT file written: %s", translated_srt_path)
    except Exception as e:
        logger.error("SRT writing failed: %s", e, exc_info=True)
        raise RuntimeError("SRT writing failed") from e

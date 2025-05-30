from datetime import timedelta
from pathlib import Path
from typing import Any, List

import srt
from src.services.translation import translate


def generate_srt_file(
    segments: List[Any], output_path: Path, language: str
) -> Path:
    """
    Generate an SRT subtitle file from a list of segments using the srt library.

    Args:
        segments (List[Any]): List of segments, each with 'start', 'end', and 'text' attributes (in seconds and str).
        output_path (Path): Base wpath (without extension) for output.
        language (str): Language code to include in the filename.

    Returns:
        Path: Path to the generated SRT file.
    """

    srt_segments = []
    for index, segment in enumerate(segments, start=1):
        start_sec = (
            segment["start"] if isinstance(segment, dict) else segment.start
        )
        end_sec = segment["end"] if isinstance(segment, dict) else segment.end
        text = segment["text"] if isinstance(segment, dict) else segment.text
        srt_segments.append(
            srt.Subtitle(
                index=index,
                start=timedelta(seconds=float(start_sec)),
                end=timedelta(seconds=float(end_sec)),
                content=text,
            )
        )
    srt_text = srt.compose(srt_segments)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_text)
    return output_path


def generate_translated_srt_file(
    segments: List[Any], output_path: Path, source_lang: str, target_lang: str
) -> Path:
    """
    Generate an SRT subtitle file from a list of segments using the srt library.

    Args:
        segments (List[Any]): List of segments, each with 'start', 'end', and 'text' attributes (in seconds and str).
        output_path (Path): Base wpath (without extension) for output.
        language (str): Language code to include in the filename.

    Returns:
        Path: Path to the generated SRT file.
    """

    srt_segments = []
    for index, segment in enumerate(segments, start=1):
        start_sec = (
            segment["start"] if isinstance(segment, dict) else segment.start
        )
        end_sec = segment["end"] if isinstance(segment, dict) else segment.end
        text = segment["text"] if isinstance(segment, dict) else segment.text
        translated_text = translate(
            text=text, source_lang=source_lang, target_lang=target_lang
        )
        srt_segments.append(
            srt.Subtitle(
                index=index,
                start=timedelta(seconds=float(start_sec)),
                end=timedelta(seconds=float(end_sec)),
                content=translated_text,
            )
        )
    srt_text = srt.compose(srt_segments)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_text)
        f.close()
    return output_path

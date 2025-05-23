from typing import List, Tuple

from faster_whisper import WhisperModel


def transcribe(audio_path: str, model_size: str = "small") -> Tuple[str, List]:
    model = WhisperModel(model_size, compute_type="float32")
    segments, info = model.transcribe(audio_path)
    language = info.language
    return language, list(segments)


def format_time(seconds: float) -> str:
    ms = round((seconds - int(seconds)) * 1000)
    h, remainder = divmod(int(seconds), 3600)
    m, s = divmod(remainder, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def generate_subtitle_file(
    input_video: str, language: str, segments: List
) -> str:
    from pathlib import Path

    input_stem = Path(input_video).stem
    srt_filename = f"{input_stem}.{language}.srt"
    with open(srt_filename, "w", encoding="utf-8") as f:
        for idx, seg in enumerate(segments, 1):
            start = format_time(seg.start)
            end = format_time(seg.end)
            f.write(f"{idx}\n{start} --> {end}\n{seg.text.strip()}\n\n")
    return srt_filename

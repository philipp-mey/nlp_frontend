from typing import List, Tuple

from faster_whisper import WhisperModel


def transcribe(audio_path: str, model_size: str = "small") -> Tuple[str, List]:
    model = WhisperModel(model_size, compute_type="float32")
    segments, info = model.transcribe(audio_path)
    language = info.language
    return language, list(segments)

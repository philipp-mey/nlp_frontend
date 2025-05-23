from pathlib import Path

import ffmpeg


def extract_audio(input_video: str) -> str:
    """
    Extracts audio from a video file and saves as WAV.
    Returns the path to the audio file.
    """
    audio_path = Path(input_video).with_suffix(".wav")
    (
        ffmpeg.input(input_video)
        .output(str(audio_path), acodec="pcm_s16le", ac=1, ar="16k")
        .run(overwrite_output=True, quiet=True)
    )
    return str(audio_path)

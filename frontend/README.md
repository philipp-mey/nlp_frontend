# Easy-NLP-Translate Video Processing and Translation App

This project provides a complete video processing and translation pipeline built around the `easy-nlp-translate` PyPi package. It allows users to upload videos, extract audio, transcribe subtitles, translate them into multiple languages, and download the translated subtitle files. The app includes both a backend for processing tasks and a frontend for user interaction.

---

## Features

- **Upload videos** in various formats (e.g., MP4, AVI, MOV) up to 500MB.
- **Audio extraction** from uploaded videos.
- **Subtitle transcription** in the video's original language.
- **Subtitle translation** into multiple supported languages.
- **Download options** for original and translated subtitle files.
- **Video library** to browse processed videos and watch them with subtitles.

---

## Project Structure

``` tree
.
├── backend
│   ├── demo_video.mp4
│   ├── Dockerfile
│   ├── main.py
│   ├── media
│   │   ├── processed
│   │   │   ├── 5a01ce63-12ff-4a3c-8535-c5872865f2d2
│   │   │   │   ├── What is GitHub.de.srt
│   │   │   │   ├── What is GitHub.mp4
│   │   │   │   └── What is GitHub.srt
│   │   │   └── ...
│   │   └── uploads
│   ├── pyproject.toml
│   ├── README.md
│   ├── src
│   │   ├── bff_api
│   │   │   ├── __init__.py
│   │   │   ├── root.py
│   │   │   └── v1
│   │   │       ├── __init__.py
│   │   │       ├── main_router.py
│   │   │       ├── upload.py
│   │   │       └── video.py
│   │   ├── processing
│   │   │   └── pipeline.py
│   │   └── services
│   │       ├── __init__.py
│   │       ├── audio.py
│   │       ├── file_utils.py
│   │       ├── srt_writer.py
│   │       ├── transcription.py
│   │       └── translation.py
│   ├── test.py
│   └── uv.lock
├── docker-compose.yaml
├── frontend
│   ├── Dockerfile
│   ├── main.py
│   ├── pyproject.toml
│   ├── README.md
│   ├── src
│   │   ├── app.py
│   │   ├── images
│   │   │   └── pypi_package.png
│   │   ├── pages
│   │   │   ├── 1_⬆️_Upload.py
│   │   │   └── 2_🎬_Library.py
│   │   └── utils
│   │       └── page_setup.py
│   └── uv.lock
├── LICENSE
└── ruff.toml
```

---

## Installation and Setup

### Prerequisites

- **Python 3.11 or 3.12**
- **Docker** and **Docker Compose**

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/easy-nlp-translate-app.git
   cd easy-nlp-translate-app

2. Build and run the app with Docker Compose:

   ``` bash
   docker-compose up --build
   ```

3. Access the app at http://localhost:8501 (frontend) and http://localhost:8000/docs (backend).

### Usage

1. Upload Videos: Use the "Upload" page to upload videos and select a target translation language.
2. Processing: The backend will process the video, extract audio, transcribe subtitles, and translate them. (This can take a while - so just grab a coffee in the meantime)
3. Download Files: Download both the original and translated subtitles from the "Library" page.
Watch Videos: View processed videos with subtitles directly in the app.

### License

This project is licensed under the MIT license.

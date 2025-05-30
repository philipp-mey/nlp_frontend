FROM ubuntu:24.04

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY media/ media/
COPY src/ src/
COPY main.py main.py
COPY pyproject.toml pyproject.toml

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "main.py"]
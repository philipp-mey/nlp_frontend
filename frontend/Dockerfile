FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY .streamlit/ .streamlit
COPY src/ src
COPY main.py main.py
COPY pyproject.toml pyproject.toml

RUN uv sync

EXPOSE 8501

CMD ["uv", "run", "main.py"]
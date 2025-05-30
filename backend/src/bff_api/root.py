from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .v1 import v1


class Tags:
    HEALTH = "Health"
    ROOT = "Root"


app = FastAPI(title="NLP Frontend API")

app.include_router(v1, prefix="/v1")
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/health", tags=[Tags.HEALTH])
async def health_check():
    return {"status": "healthy"}


@app.get("/", tags=[Tags.ROOT])
async def root():
    return {"message": "Welcome to the NLP Frontend API"}

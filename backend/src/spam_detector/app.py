"""
The entrypoint for the FastAPI application.
"""

from uuid import UUID

from fastapi import FastAPI, HTTPException

from spam_detector.interfaces import (
    DetectRequestPayload,
    DetectResponse,
    HealthResponse,
)
from spam_detector.services import get_youtube_comments

app = FastAPI()

APP_VERSION = "0.1.0"


@app.get("/v1/health")
def get_health() -> HealthResponse:
    """
    The root endpoint for the FastAPI application.

    Returns the current version and the status of the application.
    """

    return HealthResponse(version=APP_VERSION, status="ok")


@app.post("/v1/detect")
def detect_text(payload: DetectRequestPayload) -> DetectResponse:
    """
    Given a YouTube comment content, determines if the content is spam or not.
    """
    try:
        if payload.uuid is None:
            uuid = UUID(int=0)
        else:
            uuid = payload.uuid

        if not payload.content:
            raise ValueError("Content field is required")

        # FIXME: implement the spam detection logic
        is_spam = True

        return DetectResponse(uuid=uuid, is_spam=is_spam)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/v1/process_page/{video_id}")
def process_page(video_id: str):
    """
    Given a YouTube video ID, get first 100 comments and return the detection
    results in batch.
    """

    try:
        comments = get_youtube_comments(video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    results: list[DetectResponse] = []
    for comment in comments:
        uuid = UUID(int=0)
        is_spam = detect_text(DetectRequestPayload(uuid=uuid, content=comment)).is_spam
        results.append(DetectResponse(uuid=uuid, is_spam=is_spam))

    return results

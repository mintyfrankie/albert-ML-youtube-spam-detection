"""
The entrypoint for the FastAPI application.
"""

from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query

from spam_detector.interfaces import (
    DetectRequestPayload,
    DetectResponse,
    HealthResponse,
    VideoResponse,
)
from spam_detector.services import detect_spam, get_youtube_comments

app = FastAPI()

APP_VERSION = "0.1.0"


@app.get("/v1/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """
    Get the health status of the application.

    Returns:
        HealthResponse: The current version and status of the application.
    """
    return HealthResponse(version=APP_VERSION, status="ok")


@app.post("/v1/detect", response_model=DetectResponse)
async def detect_text(payload: DetectRequestPayload) -> DetectResponse:
    """
    Determine if a YouTube comment is spam or not.

    Args:
        payload (DetectRequestPayload): The request payload containing the comment content.

    Returns:
        DetectResponse: The detection result.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        # FIXME: should generate a random UUID
        uuid = payload.uuid or UUID(int=0)

        if not payload.content.strip():
            raise ValueError("Content field is required and cannot be empty")

        is_spam = await detect_spam(payload.content)
        return DetectResponse(uuid=uuid, is_spam=is_spam)

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/v1/process_page/{video_id}", response_model=VideoResponse)
async def process_page(
    video_id: str,
    max_results: int = Query(
        default=50, ge=1, le=100, description="Number of comments to process"
    ),
) -> VideoResponse:
    """
    Process comments from a YouTube video and detect spam.

    Args:
        video_id (str): The YouTube video ID.
        max_results (int): The maximum number of comments to process (1-100).

    Returns:
        VideoResponse: The processed comments with spam detection results.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        comments = await get_youtube_comments(video_id, max_results)
        results: List[DetectResponse] = []

        for comment in comments:
            uuid = UUID(int=0)
            is_spam = await detect_spam(comment)
            results.append(DetectResponse(uuid=uuid, is_spam=is_spam))

        return VideoResponse(id=video_id, nb=len(results), comments=results)

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
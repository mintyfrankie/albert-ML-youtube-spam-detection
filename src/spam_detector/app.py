"""
The entrypoint for the FastAPI application.
"""

from fastapi import FastAPI

from spam_detector.interfaces import HealthResponse

app = FastAPI()

APP_VERSION = "0.1.0"


@app.get("/")
def read_root() -> HealthResponse:
    """
    The root endpoint for the FastAPI application.

    Returns the current version and the status of the application.
    """

    return HealthResponse(version=APP_VERSION, status="ok")


@app.post("/detect_text")
def detect_text():
    """
    Given a YouTube comment content, determines if the content is spam or not.
    """

    raise NotImplementedError("Not implemented yet")


@app.post("/process_page")
def process_page():
    """
    Given a YouTube video URL, processes the video page and returns the comments.
    """

    raise NotImplementedError("Not implemented yet")

"""
The entrypoint for the FastAPI application.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """
    The root endpoint for the FastAPI application.

    Returns the current version and the status of the application.
    """

    raise NotImplementedError("Not implemented yet")


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

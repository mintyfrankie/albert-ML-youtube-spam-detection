import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_youtube_comments(video_id: str, max_results: int = 50) -> list[str]:
    """
    Given a YouTube video ID, get first 100 comments.
    """

    YOUTUBE_API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
    BASE_URL = "https://www.googleapis.com/youtube/v3/commentThreads"

    try:
        results = (
            requests.get(
                BASE_URL,
                params={
                    "key": YOUTUBE_API_KEY,
                    "textFormat": "plainText",
                    "part": "snippet",
                    "videoId": video_id,
                    "maxResults": max_results,
                },
            )
            .json()
            .get("items")
        )
        return [
            x["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for x in results
        ]
    except Exception as e:
        raise e

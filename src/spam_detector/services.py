import os

import requests
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3/commentThreads"


async def get_youtube_comments(video_id: str, max_results: int = 50) -> list[str]:
    """
    Get comments from a YouTube video.

    Args:
        video_id (str): The YouTube video ID.
        max_results (int): The maximum number of comments to retrieve.

    Returns:
        List[str]: A list of comment texts.

    Raises:
        Exception: If there's an error fetching the comments.
    """
    try:
        response = requests.get(
            BASE_URL,
            params={
                "key": YOUTUBE_API_KEY,
                "textFormat": "plainText",
                "part": "snippet",
                "videoId": video_id,
                "maxResults": max_results,
            },
        )
        response.raise_for_status()
        results = response.json().get("items", [])
        return [
            x["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for x in results
        ]
    except requests.RequestException as e:
        raise Exception(f"Error fetching YouTube comments: {str(e)}")


async def detect_spam(model, content: str) -> bool:
    """
    Detect if a comment is spam.

    Args:
        content (str): The content of the comment.

    Returns:
        bool: True if the comment is spam, False otherwise.
    """

    THRESHOLD = 0.5
    prob = model.predict_proba([content])[0][1]
    return prob > THRESHOLD

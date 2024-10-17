import os

import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
YOUTUBE_VIDEO_ID = "hwP7WQkmECE"

BASE_URL = "https://www.googleapis.com/youtube/v3/commentThreads"

results = (
    requests.get(
        BASE_URL,
        params={
            "key": YOUTUBE_API_KEY,
            "textFormat": "plainText",
            "part": "snippet",
            "videoId": YOUTUBE_VIDEO_ID,
            "maxResults": 50,
        },
    )
    .json()
    .get("items")
)

[x["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for x in results]

"""
Test cases for the FastAPI application in app.py.
"""

from typing import TYPE_CHECKING
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from spam_detector.app import app
from spam_detector.interfaces import DetectRequestPayload, DetectResponse, VideoResponse

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

client = TestClient(app)


def test_get_health() -> None:
    """
    Test the health endpoint to ensure it returns the correct version and status.
    """
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0", "status": "ok"}


@pytest.mark.asyncio
async def test_detect_text_not_spam(mocker: "MockerFixture") -> None:
    """
    Test the detect endpoint with non-spam content.

    Args:
        mocker: Pytest fixture for mocking.
    """
    mocker.patch("spam_detector.app.detect_spam", return_value=False)
    uuid = UUID("00000000-0000-0000-0000-000000000000")
    payload = DetectRequestPayload(content="This is not spam", uuid=uuid)
    response = client.post(
        "/v1/detect", json={"content": payload.content, "uuid": str(payload.uuid)}
    )
    assert response.status_code == 200
    assert response.json() == {
        "uuid": str(uuid),
        "is_spam": False,
    }


@pytest.mark.asyncio
async def test_detect_text_spam(mocker: "MockerFixture") -> None:
    """
    Test the detect endpoint with spam content.

    Args:
        mocker: Pytest fixture for mocking.
    """
    mocker.patch("spam_detector.app.detect_spam", return_value=True)
    uuid = UUID("12345678-1234-5678-1234-567812345678")
    payload = DetectRequestPayload(content="Buy cheap products now!", uuid=uuid)
    response = client.post(
        "/v1/detect", json={"content": payload.content, "uuid": str(payload.uuid)}
    )
    assert response.status_code == 200
    assert response.json() == {
        "uuid": str(uuid),
        "is_spam": True,
    }


@pytest.mark.asyncio
async def test_detect_text_empty_content() -> None:
    """
    Test the detect endpoint with empty content to ensure it raises an error.
    """
    uuid = UUID("00000000-0000-0000-0000-000000000000")
    payload = DetectRequestPayload(content="", uuid=uuid)
    response = client.post(
        "/v1/detect", json={"content": payload.content, "uuid": str(payload.uuid)}
    )
    assert response.status_code == 422
    assert "Content field is required and cannot be empty" in response.json()["detail"]


@pytest.mark.asyncio
async def test_detect_text_internal_error(mocker: "MockerFixture") -> None:
    """
    Test the detect endpoint when an internal error occurs.

    Args:
        mocker: Pytest fixture for mocking.
    """
    mocker.patch(
        "spam_detector.app.detect_spam", side_effect=Exception("Internal error")
    )
    uuid = UUID("00000000-0000-0000-0000-000000000000")
    payload = DetectRequestPayload(content="Test content", uuid=uuid)
    response = client.post(
        "/v1/detect", json={"content": payload.content, "uuid": str(payload.uuid)}
    )
    assert response.status_code == 500
    assert "Internal server error" in response.json()["detail"]


@pytest.mark.asyncio
async def test_process_page_success(mocker: "MockerFixture") -> None:
    """
    Test the process_page endpoint with successful comment retrieval and processing.

    Args:
        mocker: Pytest fixture for mocking.
    """
    mocker.patch(
        "spam_detector.app.get_youtube_comments",
        return_value=["Comment 1", "Comment 2"],
    )
    mocker.patch("spam_detector.app.detect_spam", side_effect=[True, False])

    response = client.get("/v1/process_page/video123?max_results=2")
    assert response.status_code == 200

    expected_response = VideoResponse(
        id="video123",
        nb=2,
        comments=[
            DetectResponse(
                uuid=UUID("00000000-0000-0000-0000-000000000000"), is_spam=True
            ),
            DetectResponse(
                uuid=UUID("00000000-0000-0000-0000-000000000000"), is_spam=False
            ),
        ],
    )

    # Convert the expected response to a dict and serialize UUIDs to strings
    expected_dict = expected_response.dict()
    for comment in expected_dict["comments"]:
        comment["uuid"] = str(comment["uuid"])

    assert response.json() == expected_dict


@pytest.mark.asyncio
async def test_process_page_invalid_max_results() -> None:
    """
    Test the process_page endpoint with an invalid max_results parameter.
    """
    response = client.get("/v1/process_page/video123?max_results=101")
    assert response.status_code == 422
    error_msg = response.json()["detail"][0]["msg"]
    assert any(
        expected in error_msg
        for expected in [
            "ensure this value is less than or equal to 100",
            "Input should be less than or equal to 100",
        ]
    )


@pytest.mark.asyncio
async def test_process_page_youtube_api_error(mocker: "MockerFixture") -> None:
    """
    Test the process_page endpoint when the YouTube API raises an error.

    Args:
        mocker: Pytest fixture for mocking.
    """
    mocker.patch(
        "spam_detector.app.get_youtube_comments",
        side_effect=ValueError("Invalid video ID"),
    )

    response = client.get("/v1/process_page/invalid_video_id")
    assert response.status_code == 422
    assert "Invalid video ID" in response.json()["detail"]


@pytest.mark.asyncio
async def test_process_page_internal_error(mocker: "MockerFixture") -> None:
    """
    Test the process_page endpoint when an internal error occurs.

    Args:
        mocker: Pytest fixture for mocking.
    """
    mocker.patch(
        "spam_detector.app.get_youtube_comments",
        side_effect=Exception("Internal error"),
    )

    response = client.get("/v1/process_page/video123")
    assert response.status_code == 500
    assert "Internal server error" in response.json()["detail"]


@pytest.mark.parametrize("max_results", [1, 50, 100])
@pytest.mark.asyncio
async def test_process_page_different_max_results(
    mocker: "MockerFixture", max_results: int
) -> None:
    """
    Test the process_page endpoint with different valid max_results values.

    Args:
        mocker: Pytest fixture for mocking.
        max_results: The number of comments to process.
    """
    mocker.patch(
        "spam_detector.app.get_youtube_comments", return_value=["Comment"] * max_results
    )
    mocker.patch("spam_detector.app.detect_spam", return_value=False)

    response = client.get(f"/v1/process_page/video123?max_results={max_results}")
    assert response.status_code == 200
    assert response.json()["nb"] == max_results
    assert len(response.json()["comments"]) == max_results

import pytest
from fastapi.testclient import TestClient
from spam_detector.app import app


class TestApp:
    """
    Tests the FastAPI application
    """

    @pytest.fixture
    def client(self):
        """
        Creates a TestClient instance for the FastAPI application.
        """
        return TestClient(app)

    def test_read_root(self, client):
        """
        Tests the root endpoint of the FastAPI application.
        """
        response = client.get("/v1/health")
        data = response.json()

        assert response.status_code == 200
        assert data["status"] is not None
        assert data["version"] is not None

    def test_detect_text(self, client):
        """
        Tests the detect_text endpoint of the FastAPI application.
        """

        payload = {"content": "this is an example YouTube comment."}
        response = client.post("/v1/detect", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["is_spam"] is not None

    def test_detect_with_wrong_payload(self, client):
        """
        Tests the detect_text endpoint of the FastAPI application with wrong payload.
        """

        payload = {"wrong": "field"}
        response = client.post("/v1/detect", json=payload)

        assert response.status_code == 422

    def test_process_page(self, client):
        """
        Tests the process_page endpoint of the FastAPI application.
        """

        payload = {"id": "dQw4w9WgXcQ", "first": 10}
        response = client.post("/process_page", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert payload["first"] == data["nb"]
        assert len(data["comments"]) == payload["first"]

    def test_process_page_with_wrong_payload(self, client):
        """
        Tests the process_page endpoint of the FastAPI application with wrong payload.
        """

        payload = {"wrong": "field"}
        response = client.post("/process_page", json=payload)

        assert response.status_code == 422

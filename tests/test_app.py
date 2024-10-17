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
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"version": "0.1.0", "status": "ok"}

    def test_detect_text(self, client):
        """
        Tests the detect_text endpoint of the FastAPI application.
        """

        # TODO: implement the test
        response = client.post("/detect_text")
        assert response.status_code == 501
        assert response.json() == {"detail": "Not implemented yet"}

    def test_process_page(self, client):
        """
        Tests the process_page endpoint of the FastAPI application.
        """

        # TODO: implement the test
        response = client.post("/process_page")
        assert response.status_code == 501
        assert response.json() == {"detail": "Not implemented yet"}

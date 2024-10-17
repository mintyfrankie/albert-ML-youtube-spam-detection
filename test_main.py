from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0", "status": "ok"}


def test_detect_text():
    response = client.post("/detect_text")
    assert response.status_code == 501
    assert response.json() == {"detail": "Not implemented yet"}


def test_process_page():
    response = client.post("/process_page")
    assert response.status_code == 501
    assert response.json() == {"detail": "Not implemented yet"}

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_route():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_text_schedule_route_success():
    payload = {
        "text": "Book dentist next Friday at 3pm",
        "reference_date": "2025-09-20"
    }
    response = client.post("/api/v1/schedule/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["appointment"]["department"] == "Dentistry"
    assert data["appointment"]["date"] == "2025-09-26"
    assert data["appointment"]["time"] == "15:00"

def test_text_schedule_route_ambiguous():
    payload = {"text": "Book appointment next week"}
    response = client.post("/api/v1/schedule/text", json=payload)
    data = response.json()
    assert data["status"] == "needs_clarification"
    assert data["message"] == "Ambiguous date/time or department"

def test_image_schedule_route():
    with open("samples/sample_appointment_note.png", "rb") as f:
        response = client.post(
            "/api/v1/schedule/image",
            files={"file": ("sample_appointment_note.png", f, "image/png")},
            data={"reference_date": "2025-09-20"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["appointment"]["department"] == "Dentistry"

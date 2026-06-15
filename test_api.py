from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"].lower()


def test_evaluate_valid_request():
    payload = {
        "reference_answer": "Photosynthesis is the process by which plants convert sunlight into glucose.",
        "student_answer": "Plants use sunlight to make glucose through photosynthesis.",
        "max_score": 10
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "score" in data
    assert "max_score" in data
    assert "percentage" in data
    assert "matched_keywords" in data
    assert "missed_keywords" in data
    assert "total_keywords" in data
    assert "feedback" in data


def test_evaluate_score_range():
    payload = {
        "reference_answer": "The mitochondria is the powerhouse of the cell.",
        "student_answer": "Cells have a nucleus.",
        "max_score": 10
    }
    response = client.post("/evaluate", json=payload)
    data = response.json()
    assert 0 <= data["score"] <= 10


def test_evaluate_empty_student_answer():
    payload = {
        "reference_answer": "Plants need sunlight and water to grow.",
        "student_answer": "",
        "max_score": 10
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    assert response.json()["score"] == 0


def test_evaluate_missing_field():
    payload = {
        "reference_answer": "Some reference"
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 422


def test_evaluate_custom_max_score():
    payload = {
        "reference_answer": "oxygen carbon water",
        "student_answer": "oxygen carbon water",
        "max_score": 50
    }
    response = client.post("/evaluate", json=payload)
    data = response.json()
    assert data["max_score"] == 50
    assert data["score"] <= 50


def test_batch_evaluate():
    payload = [
        {
            "reference_answer": "Water is made of hydrogen and oxygen.",
            "student_answer": "Water has hydrogen and oxygen atoms.",
            "max_score": 10
        },
        {
            "reference_answer": "The earth revolves around the sun.",
            "student_answer": "Earth goes around the sun.",
            "max_score": 10
        }
    ]
    response = client.post("/evaluate/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_evaluated"] == 2
    assert len(data["results"]) == 2
from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Enterprise RAG Agent API is running"


def test_valid_question():
    response = client.post(
        "/ask",
        json={
            "question": "How many casual leave days do employees get?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "tool" in data
    assert "sources" in data

    assert "12 casual leave" in data["answer"]


def test_empty_question():
    response = client.post(
        "/ask",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


def test_short_question():
    response = client.post(
        "/ask",
        json={
            "question": "Hi"
        }
    )

    assert response.status_code == 422
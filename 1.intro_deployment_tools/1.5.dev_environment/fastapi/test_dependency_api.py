from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from dependency_api import app, get_http_client


def get_fake_client():
    fake_response = MagicMock()
    fake_response.json.return_value = {"fact": "test_fact"}
    fake_response.status_code = 200
    fake_session = MagicMock()
    fake_session.get.return_value = fake_response
    return fake_session

app.dependency_overrides[get_http_client] = get_fake_client

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_get_cat_fact():
    response = client.get("/cat_facts")

    assert response.status_code == 200
    assert response.json()["fact"] == "test_fact"
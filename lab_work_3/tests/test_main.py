import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app 
import datetime
from models import Session

client = TestClient(app)

@pytest.fixture
def mock_session():
    return Session(id=1, expiration_timestamp=datetime.datetime.now() + datetime.timedelta(hours=1))

@pytest.fixture
def expired_session():
    return Session(id=1, expiration_timestamp=datetime.datetime.now() - datetime.timedelta(hours=1))

@patch("storage.create_session")
def test_create_session(mock_create_session, mock_session):
    # Замокать функцию storage.create_session
    mock_create_session.return_value = mock_session

    response = client.get("/session")
    assert response.status_code == 200
    assert response.json() == {"session_id": mock_session.id}

@patch("storage.get_session")
def test_create_item_valid_session(mock_get_session, mock_session):
    # Замокать функцию storage.get_session
    mock_get_session.return_value = mock_session

    session_id = mock_session.id
    response = client.get(f"/tool/{session_id}")
    assert response.status_code == 200
    assert "Your super number today is: " in response.json()

@patch("storage.get_session")
def test_create_item_session_not_found(mock_get_session):
    # Замокать функцию storage.get_session
    mock_get_session.return_value = None

    response = client.get("/tool/1")
    assert response.status_code == 200
    assert response.json() == {"error": "session not found"}

@patch("storage.get_session")
def test_create_item_expired_session(mock_get_session, expired_session):
    # Замокать функцию storage.get_session
    mock_get_session.return_value = expired_session

    response = client.get(f"/tool/{expired_session.id}")
    assert response.status_code == 200
    assert response.json() == {"error": "session expired"}

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Please request on /session and then on /tool/{session_id}'
    }
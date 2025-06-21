import pytest
from app import app, get_random_quote
from flask.testing import FlaskClient

@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    return app.test_client()

# ✅ Test 1: Homepage loads successfully
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<" in response.data  # HTML is returned

# ✅ Test 2: Quote function returns valid format (mocked)
def test_get_random_quote_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"q": "Test quote", "a": "Tester"}]
    mocker.patch("app.requests.get", return_value=mock_response)

    quote = get_random_quote()
    assert quote == "Test quote — Tester"

# ✅ Test 3: Handles failed API request gracefully
def test_get_random_quote_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("app.requests.get", return_value=mock_response)

    quote = get_random_quote()
    assert "Could not fetch quote" in quote or "Error:" in quote

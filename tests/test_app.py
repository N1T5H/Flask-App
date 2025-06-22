import sys
import os
import pytest
import importlib

# Add root project folder to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask.testing import FlaskClient

@pytest.fixture
def client():
    import app
    app.app.testing = True
    return app.app.test_client()

def test_homepage(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<" in response.data

def test_get_random_quote_success(mocker):
    # ✅ Patch before import AND reload the app module
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"q": "Test quote", "a": "Tester"}]

    mocker.patch("app.requests.get", return_value=mock_response)

    import app
    importlib.reload(app)  # ✅ Force reloading after patch

    quote = app.get_random_quote()
    assert quote == "Test quote — Tester"

def test_get_random_quote_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500

    mocker.patch("app.requests.get", return_value=mock_response)

    import app
    importlib.reload(app)  # ✅ Force reloading after patch

    quote = app.get_random_quote()
    assert "Could not fetch quote" in quote or "Error:" in quote

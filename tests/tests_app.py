import pytest
from app import app, get_random_quote
from flask import url_for

# Test client setup
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test 1: Home route returns 200
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<div class=\"quote\">" in response.data

# Test 2: Test get_random_quote with mocked API response
def test_get_random_quote_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "q": "Test quote",
        "a": "Author"
    }]
    mocker.patch('app.requests.get', return_value=mock_response)

    quote = get_random_quote()
    assert quote == "Test quote — Author"

# Test 3: Test get_random_quote with failed API call
def test_get_random_quote_failure(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch('app.requests.get', return_value=mock_response)

    quote = get_rand_

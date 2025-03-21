import requests
import pytest

BASE_URL = "https://lintech.id/whatsapp/api"

@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}

@pytest.fixture
def valid_user():
    return {"user": "silver", "pass": "silver"}

@pytest.mark.api
def test_login_api(valid_user, headers):
    response = requests.post(f"{BASE_URL}/login", json=valid_user, headers=headers)
    assert response.status_code == 200
    assert "token" in response.json()

@pytest.mark.api
def test_create_user(headers):
    data = {"user": "testuser", "pass": "testpass"}
    response = requests.post(f"{BASE_URL}/users", json=data, headers=headers)
    assert response.status_code == 201

# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser option")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.numprocesses = "auto"
import pytest
import requests
import allure

BASE_URL = "https://lintech.id/whatsapp/api"  # Ganti dengan API backend-mu

@pytest.fixture
def valid_user():
    return {"user": "silver", "pass": "silver"}

@pytest.fixture
def invalid_user():
    return {"user": "wronguser", "user": "wrongpass"}

@pytest.fixture
def headers():
    """Header standar untuk pengujian"""
    return {"Content-Type": "application/json"}

@allure.feature("Authentication")
@allure.story("Basic Authentication")
def test_basic_auth(valid_user, headers):
    """🔹 Test Basic Authentication (Username & Password)"""
    with allure.step("Mengirim request login"):
        response = requests.post(f"{BASE_URL}/login", json=valid_user, headers=headers)

    with allure.step("Memeriksa response status dan token"):
        assert response.status_code == 200
        assert "token" in response.json(), "❌ Token tidak ditemukan!"
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.JSON)

    print(f"✅ Token didapatkan: {response.json()['token']}")

@allure.feature("Authentication")
@allure.story("Invalid Login Attempt")
def test_invalid_login(invalid_user, headers):
    """🔹 Test Login Gagal"""
    response = requests.post(f"{BASE_URL}/login", json=invalid_user, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")

    with allure.step("Memeriksa bahwa login gagal"):
        assert response.status_code == 401, "❌ Harusnya login gagal!"
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)

    print("✅ Login gagal seperti yang diharapkan")

@allure.feature("Security Testing")
@allure.story("SQL Injection")
def test_sql_injection():
    """🔹 Test SQL Injection"""
    payload = {"username": "' OR '1'='1", "password": "any"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")

    with allure.step("Memeriksa apakah API rentan terhadap SQL Injection"):
        assert response.status_code == 401, "❌ Server rentan terhadap SQL Injection!"
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)

    print("✅ SQL Injection tidak berhasil!")

@allure.feature("Security Testing")
@allure.story("Cross Site Scripting (XSS)")
def test_xss():
    """🔹 Test XSS Attack"""
    payload = {"comment": "<script>alert('XSS!')</script>"}
    response = requests.post(f"{BASE_URL}/comments", json=payload)

    with allure.step("Memeriksa apakah API rentan terhadap XSS"):
        assert response.status_code != 200, "❌ Server rentan terhadap XSS!"
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)

    print("✅ XSS tidak berhasil!")


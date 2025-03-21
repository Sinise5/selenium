import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://lintech.id/whatsapp")
    yield driver
    driver.quit()

@pytest.mark.parametrize("username,password,expected", [
    ("silver", "silver", "success"),
    ("admin", "wrongpass", "fail"),
    ("", "", "fail")
])
def test_login(driver, username, password, expected):
    login_page = LoginPage(driver)
    login_page.login(username, password)
    assert ("dash" in driver.current_url.lower()) == (expected == "success")
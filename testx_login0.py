import logging
import os
import time
import pytest
import cv2
import numpy as np
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Konfigurasi logging
logging.basicConfig(
    filename="test_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_result(message):
    print(message)
    logging.info(message)

# Membuat folder screenshot jika belum ada
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def save_screenshot(driver, test_case_name):
    filename = f"screenshots/{test_case_name}.png"
    driver.save_screenshot(filename)
    log_result(f"📸 Screenshot disimpan: {filename}")

def preprocess_captcha(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((1, 1), np.uint8)
    clean_image = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    processed_path = "processed_captcha.png"
    cv2.imwrite(processed_path, clean_image)
    return processed_path

def read_captcha(image_path):
    processed_image = preprocess_captcha(image_path)
    captcha_text = pytesseract.image_to_string(Image.open(processed_image), config="--psm 7")
    captcha_text = ''.join(filter(str.isalnum, captcha_text))
    return captcha_text.strip()

def wait_for_element(driver, by, value, timeout=10, poll_frequency=0.5):
    wait = WebDriverWait(driver, timeout, poll_frequency)
    return wait.until(EC.presence_of_element_located((by, value)))

@pytest.fixture(params=["chrome", "firefox"])
def setup_driver(request):
    browser = request.param
    if browser == "chrome":
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(service=service, options=options)
    else:
        service = Service(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(service=service, options=options)
    
    driver.get("https://lintech.id/whatsapp")
    wait_for_element(driver, By.TAG_NAME, "body")
    yield driver
    driver.quit()

test_cases = [
    {"username": "silver", "password": "silver", "expected": "success"},
    {"username": "admin", "password": "wrongpass", "expected": "fail"},
    {"username": "", "password": "", "expected": "fail"},
    {"username": "testuser", "password": "", "expected": "fail"},
    {"username": "unknown", "password": "123456", "expected": "fail"},
]

@pytest.mark.parametrize("test_data", test_cases)
def test_login(setup_driver, test_data):
    driver = setup_driver
    username, password, expected = test_data["username"], test_data["password"], test_data["expected"]
    
    log_result(f"\n🔹 [TEST] Login dengan Username: {username} | Password: {password}")
    
    try:
        captcha_element = wait_for_element(driver, By.XPATH, "//img[@id='capt_01']")
        captcha_element.screenshot("captcha.png")
        captcha_text = read_captcha("captcha.png")
        log_result(f"CAPTCHA yang dibaca: {captcha_text}")
        
        username_input = wait_for_element(driver, By.NAME, "user")
        username_input.clear()
        username_input.send_keys(username)
        
        password_input = wait_for_element(driver, By.NAME, "pass")
        password_input.clear()
        password_input.send_keys(password)
        
        captcha_input = wait_for_element(driver, By.NAME, "captcha01")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)
        
        login_button = wait_for_element(driver, By.ID, "login")
        login_button.click()
        
        time.sleep(3)
        
        if "dash" in driver.current_url.lower():
            assert expected == "success", "Login berhasil padahal tidak seharusnya"
            log_result("✅ Login Berhasil!")
        else:
            assert expected == "fail", "Login gagal padahal seharusnya berhasil"
            log_result("❌ Login Gagal!")
            save_screenshot(driver, f"failed_test_{username}")
    
    except Exception as e:
        log_result(f"⚠ Error pada test case {username}: {e}")
        save_screenshot(driver, f"error_test_{username}")
